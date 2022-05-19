from itertools import zip_longest

import pyparsing
import pytest

import bootstraparse.modules.syntax as sy
from bootstraparse.modules.tools import __GL, __module_path, find_variables_in_file  # , find_functions_in_file, find_classes_in_file

ptp = pytest.param
__XF = pytest.mark.xfail


##############################################################################################################
# Utility functions
##############################################################################################################
def likely_definition(list_expression, file):
    """
    Returns a dict for each expression and the associated line where this expression is likely to be defined.
    :param list_expression: list of expressions
    :param file: file to search in
    :return: dict of expression and line
    """
    likely_definition_dict = {}
    loop_list = [e for e in list_expression]
    with open(file) as f:
        for line_number, line in enumerate(f):
            for expression_id, expression in enumerate(loop_list):
                if expression in line:
                    likely_definition_dict[expression] = line_number+1
                    loop_list.remove(expression)
    return likely_definition_dict, file


##############################################################################################################
# Error Classes
##############################################################################################################
class ReturnArgumentSizeError(Exception):
    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual

    def __str__(self):
        return f"Expected {self.expected} arguments, got {self.actual}"


##############################################################################################################
# PRE-PARSER
##############################################################################################################
# Dictionary of all label and associated token used in the Pre_parser
list_of_token_types = {
    "alias": sy.AliasToken,
    "image": sy.ImageToken,
}

# Dictionary of all lexical elements and a list of matching strings for the Pre_parser
# test_expression_matching
expressions_to_match = {
    # Base elements
    "quotes": ["'hi, there'", "'hi, there'"],
    "value": ["0.1", "'hello'"],
    "assignation": ["a=1", "a=1.33", "tr2='hu'", "val_2=2"],

    # Composite elements
    "var": ['["a"]',
            '[a=12]',
            '[a=12, b=13]',
            '[12,"a",1.1,a=12, b=13, c=14]',
            ],

    # Specific elements
    "image_element": ["@{image}", "@{image123_456}"],
    "alias_element": ["@[alias]", "@[alias123_456]"],
    "expression": ["a+b+c"],
    "html_insert": ['{test=12, 22=3, "=5}', "{testing=12, 22=3, 4=5, 6='7'}"],

    # Optional elements
    "optional": ["[a=1]", "[a=1, b=2]",
                 "{a=1'\";}",
                 "[a=1, b='2', 43, 'eee']",
                 "[a=1, b='2', 43, 'eee'] {azer=,;}",
                 "{{a=1, b='2', 43, 'eee'}}",
                 "{{a=1, b='2', 43, 'eee'}} {azer=,;}",
                 "{{a=1, b='2', 43, 'eee'}} {azer=,;} [azer=,;]",
                 "[a=1, b='2', 43, 'eee'] {azer=,;} {{azer=,;}}",
                 ],


    # Pre_parser elements
    "image": ["@{image.png}{test=22}[a=12,22,c,d,ERE,r,3]", "@{image123_456}{a=12,22,c,d,ERE,r,3}",
              "@{image123_456}[a=12,22,c,d,ERE,r,3]"],
    "alias": ["@[alias]{test=22}[a=12,22,c,d,ERE,r,3]", "@[alias123_456]{a=12,22,c,d,ERE,r,3}",
              "@[alias123_456]{a=12,22,c,d,ERE,r,3]"],

    # Syntax elements
    "line_to_replace": ["@{image}",
                        "@{image}{é=12}",
                        "@{image}{test=22}",
                        "@{image}{test=22}[a=12,22,c,d,ERE,r,3]",
                        "@[alias]{test=22}[a=12,22,c,d,ERE,r,3]",
                        ],

}

##############################################################################################################
# PARSER
##############################################################################################################

# Testing the parser lexical elements
# test_advanced_expression_and_token_creation
dict_advanced_syntax_input_and_expected_output = {
    # Enhanced text
    "et_em": [
        # Single em element, should only match the first "*"
        ("*", (sy.EtEmToken(["*"]),), __GL()),
    ],
    "et_strong": [
        # Single strong element, should only match the first "**"
        ("**", (sy.EtStrongToken(["**"]),), __GL()),
    ],
    "et_underline": [
        # Single underline element, should only match the first "__"
        ("__", (sy.EtUnderlineToken(["__"]),), __GL()),
    ],
    "et_strikethrough": [
        # Single strikethrough element, should only match the first "~~"
        ("~~", (sy.EtStrikethroughToken(["~~"]),), __GL()),
    ],
    "et_custom_span": [
        # Single custom span element, should only match the first "(#number)"
        ("(#12345)", (sy.EtCustomSpanToken(["12345"]),), __GL()),
    ],
    "il_link": [
        # Single link element, should only match the first "[link_name]('link')"
        ("[text_link]('text://www.website.com/link.html')",
         [sy.HyperlinkToken(["[text_link]('text://www.website.com/link.html')"])], __GL())
    ],
    "assignation": [
        # Single assignation element, should only match the first "a=1"
        ("a=1", [sy.BeAssignToken([["a", 1]]), ], __GL()),
        ("a='str'", [sy.BeAssignToken([["a", 'str']]), ], __GL()),
    ],
    "var": [
        # List of variables or assignations, should match "[a=12, b=13, 'c']"
        ("[a_12=12, b=13, 'c']", [
            sy.BeAssignToken([["a_12", 12]]),
            sy.BeAssignToken([["b", 13]]),
            sy.BeValueToken(["c"]),
        ], __GL()),
        ("[a=12, b=13, 'c', d=14]", [
            sy.BeAssignToken([["a", 12]]),
            sy.BeAssignToken([["b", 13]]),
            sy.BeValueToken(["c"]),
            sy.BeAssignToken([["d", 14]]),
        ], __GL()),
    ],
    "optional": [
        # Optional element, should match any optional element
        ("[a=12, b=13, 'c']", [
            sy.OptionalToken([
                sy.OptionalVarToken([
                    sy.BeAssignToken([["a", 12]]),
                    sy.BeAssignToken([["b", 13]]),
                    sy.BeValueToken(["c"]),
                ]),
            ]),
        ], __GL()),
        ("[a=12, b=13, 'c', d=14]", [
            sy.OptionalToken([
                sy.OptionalVarToken([
                    sy.BeAssignToken([["a", 12]]),
                    sy.BeAssignToken([["b", 13]]),
                    sy.BeValueToken(["c"]),
                    sy.BeAssignToken([["d", 14]]),
                ]),
            ]),
        ], __GL()),
        ("[a=12]{aze,/.}", (
            sy.OptionalToken([
                sy.OptionalVarToken([
                    sy.BeAssignToken([["a", 12]]),
                ]),
                sy.OptionalInsertToken([
                    "aze,/.",
                ]),
            ]),
        ), __GL()),
        ("{aze,/.__}[a=12]", (
            sy.OptionalToken([
                sy.OptionalInsertToken([
                    "aze,/.__",
                ]),
                sy.OptionalVarToken([
                    sy.BeAssignToken([["a", 12]]),
                ]),
            ]),
        ), __GL()),
        ("{aze!=}", (
            sy.OptionalToken([
                sy.OptionalInsertToken([
                    "aze!=",
                ]),
            ]),
        ), __GL()),
        ("{{aze!=}}", (
            sy.OptionalToken([
                sy.OptionalClassToken([
                    "aze!=",
                ]),
            ]),
        ), __GL()),
        ("{{aze!=}}{azett!=}", (
            sy.OptionalToken([
                sy.OptionalClassToken([
                    "aze!=",
                ]),
                sy.OptionalInsertToken([
                    "azett!=",
                ]),
            ]),
        ), __GL()),
        ("{{aze!=}}{azett!=}[a_32=12]", (
            sy.OptionalToken([
                sy.OptionalClassToken([
                    "aze!=",
                ]),
                sy.OptionalInsertToken([
                    "azett!=",
                ]),
                sy.OptionalVarToken([
                    sy.BeAssignToken([["a_32", 12]]),
                ]),
            ]),
        ), __GL()),
        ("[_a=12]{aze,/.}{{azer!=}}", (
            sy.OptionalToken([
                sy.OptionalVarToken([
                    sy.BeAssignToken([["_a", 12]]),
                ]),
                sy.OptionalInsertToken([
                    "aze,/.",
                ]),
                sy.OptionalClassToken([
                    "azer!=",
                ]),
            ]),
        ), __GL()),
    ],
    # Enhanced Text
    "enhanced_text": [
        # Matches a line of text, with or without inline elements
        ("*test*", (sy.EtEmToken(["*"]), sy.TextToken(["test"]), sy.EtEmToken(["*"])), __GL()),
        ("**test**", (sy.EtStrongToken(["**"]), sy.TextToken(["test"]), sy.EtStrongToken(["**"])), __GL()),
        ("__test__", (sy.EtUnderlineToken(["__"]), sy.TextToken(["test"]), sy.EtUnderlineToken(["__"])), __GL()),
        ("~~test~~", (sy.EtStrikethroughToken(["~~"]), sy.TextToken(["test"]), sy.EtStrikethroughToken(["~~"])), __GL()),
        ("(#12345)", (sy.EtCustomSpanToken(["12345"]),), __GL()),
        ("*test*test*", (sy.EtEmToken(["*"]), sy.TextToken(["test"]), sy.EtEmToken(["*"]), sy.TextToken(["test"]),
                         sy.EtEmToken(["*"])), __GL()),
        ("**test**test**",
         (sy.EtStrongToken(["**"]), sy.TextToken(["test"]), sy.EtStrongToken(["**"]), sy.TextToken(["test"]),
          sy.EtStrongToken(["**"]),), __GL()),
        ("__test__test__", (sy.EtUnderlineToken(["__"]), sy.TextToken(["test"]), sy.EtUnderlineToken(["__"]),
                            sy.TextToken(["test"]), sy.EtUnderlineToken(["__"]),), __GL()),
        ("~~test~~test~~", (sy.EtStrikethroughToken(["~~"]), sy.TextToken(["test"]), sy.EtStrikethroughToken(["~~"]),
                            sy.TextToken(["test"]), sy.EtStrikethroughToken(["~~"]),), __GL()),
        ("(#12345)test(#12345)", (sy.EtCustomSpanToken(["12345"]), sy.TextToken(["test"]),
                                  sy.EtCustomSpanToken(["12345"]),), __GL()),
        ("__test(#12)test**test__test~~", (sy.EtUnderlineToken(["__"]), sy.TextToken(["test"]),
                                           sy.EtCustomSpanToken(["12"]), sy.TextToken(["test"]),
                                           sy.EtStrongToken(["**"]),
                                           sy.TextToken(["test"]), sy.EtUnderlineToken(["__"]),
                                           sy.TextToken(["test"]), sy.EtStrikethroughToken(["~~"]),), __GL()),
        ("Test text with a link [link_name]('link')", (
            sy.TextToken(["Test text with a link"]),
            sy.HyperlinkToken(["[link_name]('link')"]),
        ), __GL()),
        ("Test text with a link [link_name](\"link\") and a *bold* text", (
            sy.TextToken(["Test text with a link"]),
            sy.HyperlinkToken(['[link_name]("link")']),
            sy.TextToken(["and a"]), sy.EtEmToken(["*"]),
            sy.TextToken(["bold"]),
            sy.EtEmToken(["*"]),
            sy.TextToken(["text"]),
        ), __GL()),
        ("Reverse order (#123) Span __ Underline ~~ Strikethrough", (
            sy.TextToken(["Reverse order"]),
            sy.EtCustomSpanToken(["123"]), sy.TextToken(["Span"]),
            sy.EtUnderlineToken(["__"]), sy.TextToken(["Underline"]),
            sy.EtStrikethroughToken(["~~"]), sy.TextToken(["Strikethrough"]),
        ), __GL()),
    ],
    "html_insert": [
        # Match an HTML insert
        ("{azer='\"}", (
            "azer='\"",
        ), __GL()),
    ],
    "class_insert": [
        # Match a class insert
        ("{{azer='\"}}", (
            "azer='\"",
        ), __GL()),
    ],
    # Structural Elements
    "se_start": [
        # Matches a start of a structural element
        ("<<div", (sy.StructuralElementStartToken(["div"]),), __GL()),
    ],
    "se_end": [
        ("div>>", (sy.StructuralElementEndToken(["div"]),), __GL()),
    ],
    "se": [
        # Matches a div element, must be at the beginning of the line, the closing div can be with arguments
        ("div>> [class='blue', 123]{var='test', number=11}", (
            sy.StructuralElementEndToken(["div"]),
            sy.OptionalToken([
                sy.OptionalVarToken([
                    sy.BeAssignToken([["class", "blue"]]),
                    sy.BeValueToken([123.0]),
                ]),
                sy.OptionalInsertToken(["var='test', number=11"]),
            ]),
        ), __GL(),),
        ("div>> [class='blue', 123]", (
            sy.StructuralElementEndToken(["div"]),
            sy.OptionalToken([
                sy.OptionalVarToken([
                    sy.BeAssignToken([["class", "blue"]]),
                    sy.BeValueToken([123.0]),
                ]),
            ]),
        ), __GL(),),

        ("div>> {var='test', number=11}", (
            sy.StructuralElementEndToken(["div"]),
            sy.OptionalToken([
                sy.OptionalInsertToken(["var='test', number=11"]),
            ]),
        ), __GL(),),
    ],

    # List Elements
    "one_olist": [
        # Matches a one-level ordered list element, must be at the beginning of the line
        # Drop the "." from the match
        ("#. Text", (sy.EtOlistToken([sy.TextToken(["Text"])]),), __GL()),
    ],
    "one_ulist": [
        # Matches a one-level unordered list element, must be at the beginning of the line
        # Drop the "-" from the match
        ("- Text", (sy.EtUlistToken([sy.TextToken(["Text"])]),), __GL()),
    ],

    # Headers
    "one_header": [
        # Matches a one-level header element, must be at the beginning of the line
        ("# Text1 #", (sy.HeaderToken(["#", "Text1 "]),), __GL()),
        ("## Text2 ##", (sy.HeaderToken(["##", "Text2 "]),), __GL()),
        ("### Text3 ###", (sy.HeaderToken(["###", "Text3 "]),), __GL()),
        ("#### Text4 ####", (sy.HeaderToken(["####", "Text4 "]),), __GL()),
        ("##### Text5 #####", (sy.HeaderToken(["#####", "Text5 "]),), __GL()),
        ("###### Text6 ######", (sy.HeaderToken(["######", "Text6 "]),), __GL()),
    ],

    # One-line display elements
    "one_display": [
        # Matches a one-level display element, must be at the beginning of the line
        ("! Display1 !", (sy.DisplayToken(["!", "Display1 "]),), __GL()),
        ("!! Display2 !!", (sy.DisplayToken(["!!", "Display2 "]),), __GL()),
        ("!!! Display3 !!!", (sy.DisplayToken(["!!!", "Display3 "]),), __GL()),
    ],

    # One-line elements
    "one_line": [
        # Matches a one-line element, must be at the beginning of the line
        ("- Text1", (sy.EtUlistToken([sy.TextToken(["Text1"])]),), __GL()),
        ("#. Text2", (sy.EtOlistToken([sy.TextToken(["Text2"])]),), __GL()),
        ("! Display3 !", (sy.DisplayToken(["!", "Display3 "]),), __GL()),
        ("!! Display4 !!", (sy.DisplayToken(["!!", "Display4 "]),), __GL()),
        ("### Text5 ###", (sy.HeaderToken(["###", "Text5 "]),), __GL()),
        ("#### Text6 ####", (sy.HeaderToken(["####", "Text6 "]),), __GL()),
        ("- Text7 [class='blue', 123]{var='test', number=11}", (
            sy.EtUlistToken([
                sy.TextToken(["Text7"]),
                sy.OptionalToken([
                    sy.OptionalVarToken([
                        sy.BeAssignToken([["class", "blue"]]),
                        sy.BeValueToken([123.0]),
                    ]),
                    sy.OptionalInsertToken(["var='test', number=11"]),
                ]),
            ]),
        ), __GL()),
        ("#. Text8 [class='blue', 123]{var='test', number=11}", (
            sy.EtOlistToken([
                sy.TextToken(["Text8"]),
                sy.OptionalToken([
                    sy.OptionalVarToken([
                        sy.BeAssignToken([["class", "blue"]]),
                        sy.BeValueToken([123.0]),
                    ]),
                    sy.OptionalInsertToken(["var='test', number=11"]),
                ]),
            ]),
        ), __GL()),
        ("! Display9 ! [class='blue', 123]{var='test', number=11}", (
            sy.DisplayToken([
                "!",
                "Display9 ",
                sy.OptionalToken([
                    sy.OptionalVarToken([
                        sy.BeAssignToken([["class", "blue"]]),
                        sy.BeValueToken([123.0]),
                    ]),
                    sy.OptionalInsertToken(["var='test', number=11"]),
                ]),
            ]),
        ), __GL()),  # Bad optional implementation
        ("## Text10 ## [class='blue', 123]{var='test', number=11}", (
            sy.HeaderToken([
                "##",
                "Text10 ",
                sy.OptionalToken([
                    sy.OptionalVarToken([
                        sy.BeAssignToken([["class", "blue"]]),
                        sy.BeValueToken([123.0]),
                    ]),
                    sy.OptionalInsertToken(["var='test', number=11"]),
                ]),
            ]),
         ), __GL()),  # Bad optional implementation
    ],

    # Tables
    "table_row": [
        # Matches a table element, must be at the beginning of the line
        ("| Text1 | Text2 |", (sy.TableRowToken([
            sy.TableCellToken([sy.TextToken(["Text1 "])]),
            sy.TableCellToken([sy.TextToken(["Text2 "])]),
        ]), ), __GL()),
        ("| Text1 | Text2 | Text3 |", (
            sy.TableRowToken([
                sy.TableCellToken([sy.TextToken(["Text1 "])]),
                sy.TableCellToken([sy.TextToken(["Text2 "])]),
                sy.TableCellToken([sy.TextToken(["Text3 "])]),
            ]),
        ), __GL()),
        ("| 2 Text1 | Text2 |", (
            sy.TableRowToken([
                sy.TableCellToken([sy.TextToken(["2 Text1 "])]),
                sy.TableCellToken([sy.TextToken(["Text2 "])]),
            ]),
        ), __GL()),
        ("|2 Text1 | Text2 |", (
            sy.TableRowToken([
                '2',
                sy.TableCellToken([sy.TextToken(["Text1 "])]),
                sy.TableCellToken([sy.TextToken(["Text2 "])]),
            ]),
        ), __GL()),
        ("|2 Text1 |3 Text2 |", (
            sy.TableRowToken([
                '2',
                sy.TableCellToken([sy.TextToken(["Text1 "])]),
                '3',
                sy.TableCellToken([sy.TextToken(["Text2 "])]),
            ]),
        ), __GL()),
        ("|2 Text1 |3 Text2 |4 Text3 |", (
            sy.TableRowToken([
                '2',
                sy.TableCellToken([sy.TextToken(["Text1 "])]),
                '3',
                sy.TableCellToken([sy.TextToken(["Text2 "])]),
                '4',
                sy.TableCellToken([sy.TextToken(["Text3 "])]),
            ]),
         ), __GL()),
        ("|3 Text1 | Text2 | {var='test', number=11}", (
            sy.TableRowToken([
                '3',
                sy.TableCellToken([sy.TextToken(["Text1 "])]),
                sy.TableCellToken([sy.TextToken(["Text2 "])]),
            ]),
            sy.OptionalToken([
                sy.OptionalInsertToken([
                    "var='test', number=11",
                ]),
            ]),
        ), __GL()),
    ],

    "table_separator": [
        # Matches a table element, must be at the beginning of the line
        ("|---|---|", (sy.TableSeparatorToken(["---", "---"]),), __GL()),
        ("|---|---|---|", (sy.TableSeparatorToken(["---", "---", "---"]),), __GL()),
        ("|:--|-:-|--:|--:|", (sy.TableSeparatorToken([":--", "-:-", "--:", "--:"]),), __GL()),
    ],

    "line": [
        # Match any line parsed by the parser (can match header, list table etc...) this is the main syntax element
        ("# Text1 #", (sy.HeaderToken(["#", "Text1 "]),), __GL()),
        ("Text *em __underline__ still em*", (
            sy.TextToken(["Text"]),
            sy.EtEmToken(["*"]),
            sy.TextToken(["em"]),
            sy.EtUnderlineToken(["__"]),
            sy.TextToken(["underline"]),
            sy.EtUnderlineToken(["__"]),
            sy.TextToken(["still em"]),
            sy.EtEmToken(["*"]),
        ), __GL(),),
        ("|2 Text1 | Text2 |", (
            sy.TableRowToken([
                "2",
                sy.TableCellToken([sy.TextToken(["Text1 "])]),
                sy.TableCellToken([sy.TextToken(["Text2 "])]),
            ]),
        ), __GL()),
        ("|---|---|", (sy.TableSeparatorToken(["---", "---"]),), __GL()),
        ("- Text", (sy.EtUlistToken([sy.TextToken(["Text"])]),), __GL()),
        ("div>>", (sy.StructuralElementEndToken(["div"]),), __GL()),
        ("#. Text with *em* and __underline__ and {arguments}{{super-arguments}}[a=1,'ui']", (
            sy.EtOlistToken([
                sy.TextToken(["Text with"]),
                sy.EtEmToken(["*"]),
                sy.TextToken(["em"]),
                sy.EtEmToken(["*"]),
                sy.TextToken(["and"]),
                sy.EtUnderlineToken(["__"]),
                sy.TextToken(["underline"]),
                sy.EtUnderlineToken(["__"]),
                sy.TextToken(["and"]),
                sy.OptionalToken([
                    sy.OptionalInsertToken([
                        "arguments",
                        ]),
                    sy.OptionalClassToken([
                        "super-arguments",
                        ]),
                    sy.OptionalVarToken([
                        sy.BeAssignToken([["a", 1]]),
                        sy.BeValueToken(["ui"]),
                        ]),
                    ]),
            ]),
        ), __GL(),),
    ],
    "blockquote": [
        ("> Text", (sy.BlockQuoteToken([sy.TextToken(["Text"])]),), __GL()),
        ("> Text with *em* and __underline__", (
            sy.BlockQuoteToken([
                sy.TextToken(["Text with"]),
                sy.EtEmToken(["*"]),
                sy.TextToken(["em"]),
                sy.EtEmToken(["*"]),
                sy.TextToken(["and"]),
                sy.EtUnderlineToken(["__"]),
                sy.TextToken(["underline"]),
                sy.EtUnderlineToken(["__"]),
            ]),
        ), __GL()),
    ],
    "blockquote_author": [
        ("> -- Author Name", (
            sy.BlockQuoteAuthorToken(["Author Name"]),
        ), __GL()),
    ],
    "quotation": [
        ("> Text", (sy.BlockQuoteToken([sy.TextToken(["Text"])]),), __GL()),
        ("> Text with *em* and __underline__", (
            sy.BlockQuoteToken([
                sy.TextToken(["Text with"]),
                sy.EtEmToken(["*"]),
                sy.TextToken(["em"]),
                sy.EtEmToken(["*"]),
                sy.TextToken(["and"]),
                sy.EtUnderlineToken(["__"]),
                sy.TextToken(["underline"]),
                sy.EtUnderlineToken(["__"]),
            ]),
        ), __GL()),
        ("> -- Author Name", (
            sy.BlockQuoteAuthorToken(["Author Name"]),
        ), __GL()),
    ],
}

# Cursed zipping oneline
zipped_dict_advanced_syntax_input_and_expected_output = [
    ptp(item[0], item[1][0], item[1][1], item[1][2], marks=item[1][3:], id=f"{item[0]} [line {item[1][2]}]") for sublist in [
        zip_longest([key], dict_advanced_syntax_input_and_expected_output[key], fillvalue=key) for key in
        dict_advanced_syntax_input_and_expected_output.keys()  # noqa E501 (line too cursed)
    ] for item in sublist
]

__syntax_file = __module_path("syntax.py")
__definition_of_syntax_elements = find_variables_in_file(__syntax_file, dict_advanced_syntax_input_and_expected_output.keys())

# test__add_tag
list_add_tag_input_and_expected_output = [
    # Test cases for the add_tag function
    # Input:
    (sy.TextToken(["Text"]), "Text"),
    (sy.EtEmToken(["*"]), "<text:em />"),
    (sy.EtStrongToken(["**"]), "<text:strong />"),
    (sy.EtUnderlineToken(["__"]), "<text:underline />"),
    (sy.EtStrikethroughToken(["~~"]), "<text:strikethrough />"),
    (sy.StructuralElementStartToken(["div"]), "<se:start = 'div' />"),
    (sy.StructuralElementEndToken(["div"]), "<se:end = 'div' />"),
    (sy.EtCustomSpanToken(["(#12)"]), "<text:custom_span = '(#12)' />"),
    (sy.HeaderToken(["#", "Text"]), "<header = '#,Text' />"),
]

# test_readable_markup
list_of_text_input_and_readable_output = [
    # Header
    ("# Text1 #", "one_header", "<header = '#,Text1 ' />"),
    ("## Text2 ##", "one_header", "<header = '##,Text2 ' />"),

    # Text
    # il_link | et_strong | et_em | et_strikethrough | et_underline | et_custom_span
    ("*Italic*", "et_em", "<text:em />"),
    ("__Underline__", "et_underline", "<text:underline />"),
    ("**Bold**", "et_strong", "<text:strong />"),
    ("~~Strikethrough~~", "et_strikethrough", "<text:strikethrough />"),
    ("Text *bold __underline__ still bold*", "enhanced_text",
     "Text <text:em /> bold <text:underline /> underline <text:underline /> still bold <text:em />"),
    # noqa E501 (line too long)
    ("[link]('http://www.google.com')", "il_link", "<hyperlink = '[link]('http://www.google.com')' />"),
    ("Reverse order: (#123) Span, __underline__ ~~strikethrough~~ **emphasis * Strong**", "enhanced_text",
     "Reverse order: <text:custom_span = '123' /> Span, <text:underline /> underline <text:underline /> <text:strikethrough /> strikethrough <text:strikethrough /> <text:strong /> emphasis <text:em /> Strong <text:strong />"), # noqa E501 (line too long)

    # Structural elements
    ("<<div", "se", "<se:start = 'div' />"),
    ("div>>", "se", "<se:end = 'div' />"),

    # Lists
    ("- Text", "one_ulist", "<list:ulist = 'Text' />"),
    ("#. Text", "one_olist", "<list:olist = 'Text' />"),

    # Tables
    ("| Text1 | Text2 |", "table", "<table:row = '<table:cell = 'Text1 ' />,<table:cell = 'Text2 ' />' />"),
    ("| Text1 |3 Text2 |", "table", "<table:row = '<table:cell = 'Text1 ' />,3,<table:cell = 'Text2 ' />' />"),
    ("|---|---|", "table_separator", "<table:separator = '---,---' />"),
    ("|:--|-:-|--:|--:|", "table_separator", "<table:separator = ':--,-:-,--:,--:' />"),

    # Other Mostly for testing and coverage
    ("'", "quotes", "'"),
]


list_of_reparsing_input_and_expected_output = [
    ("reparse_test", "enhanced_text", [sy.TextToken(["reparse_test"])], __GL()),
    ("reparse text *bold*, __underlined__ (#123) Custom", "enhanced_text", [
        sy.TextToken(["reparse text"]),
        sy.EtEmToken(["*"]),
        sy.TextToken(["bold"]),
        sy.EtEmToken(["*"]),
        sy.TextToken([","]),
        sy.EtUnderlineToken(["__"]),
        sy.TextToken(["underlined"]),
        sy.EtUnderlineToken(["__"]),
        sy.EtCustomSpanToken(["123"]),
        sy.TextToken(["Custom"])
    ], __GL())
]
final_list_of_reparsing_input_and_expected_output = [
    ptp(item[0], item[1], item[2], item[3], id=f'{item[0]} (line:{item[3]})', marks=item[4:])
    for item in list_of_reparsing_input_and_expected_output
]


@pytest.mark.parametrize("token_name,token_class", list_of_token_types.items())
def test_token_type_exists(token_name, token_class):
    """
    Test that the token type exists.
    :param token_name: The name of the token type.
    :param token_class: The class of the token type.
    :type token_name: str
    :type token_class: sy.SemanticType
    """
    assert token_class.label == token_name


def test_token_type_exists_fail():
    """
    Test that the token type does not exist.
    """
    with pytest.raises(AttributeError):
        # noinspection PyUnresolvedReferences, PyStatementEffect
        sy.UnexistingTypeToken.label == "non_existing_token"  # pylint: disable=pointless-statement


@pytest.mark.parametrize("token_class", list_of_token_types.values())
def test_of_type_creator(token_class):
    """
    Test that the of_type_creator function returns the correct type.
    :param token_class: The class of the token type.
    :type token_class: sy.SemanticType
    """
    fcr = sy.of_type(token_class)
    tnk = fcr(None, None, ['Text'])
    # noinspection PyTypeChecker
    assert isinstance(tnk, token_class)  # pylint: disable=unidiomatic-typecheck
    assert tnk.label == token_class.label


def strings_in_token(token, string_list):
    token_str = str(token)
    for string in string_list:
        if string not in token_str:
            return False
    return True


def test_semantic_type():
    """
    Test that the semantic type is correctly created.
    """
    st = sy.SemanticType("test")
    assert st.label is None
    assert strings_in_token(st, ["test", "None"])
    assert strings_in_token(repr(st), ["test", "None"])
    st = sy.SemanticType([1, 2, 3])
    assert st.label is None
    st.label = "test"
    assert strings_in_token(st, ["[1, 2, 3]", "test"])


def test_semantic_type_eq():
    """
    Test that the semantic type is correctly created.
    """
    st1 = sy.SemanticType("test")
    st2 = sy.SemanticType("test")
    assert st1 == st2
    st1 = sy.SemanticType(["test"])
    st2 = sy.SemanticType(["test2"])
    assert st1 != st2
    st1 = sy.SemanticType("test")
    st2 = sy.SemanticType([1, 2, 3])
    assert st1 != st2
    st1 = sy.SemanticType([1, 2, 3])
    st2 = sy.SemanticType([1, 2, 3])
    assert st1 == st2
    st1 = sy.SemanticType([1, 2, 3])
    st2 = sy.SemanticType([1, 2, 3, 4])
    assert st1 != st2
    st1 = sy.SemanticType([1, 2, 3, 4])
    st2 = sy.SemanticType([1, 2, 3])
    assert st1 != st2
    st1 = sy.SemanticType([1, 2, 3])
    st2 = sy.SemanticType([1, 2, 3, 4])
    assert st1 != st2
    st1 = sy.SemanticType([[1, 2, 4]])
    st2 = sy.SemanticType([[1, 2, 3]])
    assert st1 != st2


def find_expression_from_str(expression_str):
    """
    Find the expression from its string representation.
    Just trust on this one.
    :param expression_str: The string representation of the expression.
    :type expression_str: str
    :return: The expression.
    :rtype: pyparsing.ParserElement
    """
    # noinspection PyUnresolvedReferences
    return sy.__getattribute__(expression_str)  # pylint: disable=no-member


@pytest.mark.parametrize("expression,to_parse", expressions_to_match.items())
def test_expression_matching(expression, to_parse):
    """
    Test that the expression is correctly parsed.
    :param expression: The expression to test.
    :param to_parse: A list of string that should be matched by the expression.
    :type expression: str
    :type to_parse: list
    """
    expr = find_expression_from_str(expression)
    assert isinstance(expr, pyparsing.ParserElement)
    for string in to_parse:
        assert expr.parse_string(string) is not None


@pytest.mark.parametrize("markup_element, to_parse, expected, line_test", zipped_dict_advanced_syntax_input_and_expected_output)  # noqa: E501 (line too long)
def test_advanced_expression_and_token_creation(markup_element, to_parse, expected, line_test):
    """
    Test that the advanced syntax is correctly parsed and returns the correct tokens.
    :param markup_element: The expression to test.
    :param to_parse: The string to test.
    :param expected: The expected tokens.
    :param line_test: The line number of the test.
    :type markup_element: str
    :type to_parse: str
    :type expected: list
    :type line_test: int
    """
    expr = find_expression_from_str(markup_element)

    assert isinstance(expr, pyparsing.ParserElement)
    result = expr.parse_string(to_parse)
    print()
    print(f"Parsing string: '{to_parse}'")
    print("Defined at %(filename)s:%(lineno)d" % {'filename': __file__, 'lineno': line_test})
    print(f"With expression: '{markup_element}'")
    print("Defined at %(filename)s:%(lineno)d" % {'filename': __syntax_file,
                                                  'lineno': __definition_of_syntax_elements[markup_element]})
    print(f"Found: {result} (len:{len(result)}).")
    print(f"Expected: {expected} (len:{len(expected)})")
    assert result is not None
    if len(result) != len(expected):
        raise ReturnArgumentSizeError(len(expected), len(result))
    for token, expected_token in zip_longest(result, expected):
        assert token == expected_token


########################################################################################################################
# TEXT OUTPUT
########################################################################################################################
# Test the add tag function


@pytest.mark.parametrize("token, expected_output", list_add_tag_input_and_expected_output)
def test__add_tag(token, expected_output):
    """
    Test that the add_tag function works correctly.
    :param token: The token to test.
    :param expected_output: The expected output.
    :type token: sy.SemanticType
    :type expected_output: str
    """
    assert token.to_markup() == expected_output


# Test text functions
@pytest.mark.parametrize("token_list, parsing_expression, expected", list_of_text_input_and_readable_output)
def test_readable_markup(token_list, parsing_expression, expected):
    """
    Test that the readable markup is correctly generated.
    :param token_list: The list of tokens.
    :param parsing_expression: The parsing expression.
    :param expected: The expected readable markup.
    :type token_list: str
    :type parsing_expression: str
    :type expected: str
    """
    expr = find_expression_from_str(parsing_expression)
    assert isinstance(expr, pyparsing.ParserElement)
    result = expr.parse_string(token_list)
    assert result is not None
    assert sy.readable_markup(result) == expected


def test_weird_markup():
    """
    Test that the readable markup is correctly generated.
    """
    assert sy.readable_markup([sy.EmptySemanticType("weird")]) == "weird"
    empty_token = sy.SemanticType(None)
    empty_token.label = "weird"
    assert sy.readable_markup([empty_token]) == "<[NOC] weird />"

    class WeirdClass:
        def __str__(self):
            return "weird"

    assert sy.readable_markup(
        [sy.EmptySemanticType("weird"), empty_token, WeirdClass()]) == "weird <[NOC] weird /> weird"


@pytest.mark.parametrize("original_string, reparse_with, expected_output, line_test",
                         final_list_of_reparsing_input_and_expected_output)
def test_reparse(original_string, reparse_with, expected_output, line_test):
    """
    Test the reparse function
    """
    print()
    print(f"Reparsing string: '{original_string}'")
    print("Defined at %(filename)s:%(lineno)d" % {'filename': __file__, 'lineno': int(line_test)})
    print(f"With expression: '{reparse_with}'")
    print("Defined at %(filename)s:%(lineno)d" % {'filename': __syntax_file,
                                                  'lineno': __definition_of_syntax_elements[reparse_with]})
    print(f"Expected: {expected_output} (len:{len(expected_output)})")

    expression = find_expression_from_str(str(reparse_with))
    reparse_action = pyparsing.Word(pyparsing.printables+" ").add_parse_action(sy.reparse(expression))
    reparse_result = reparse_action.parseString(str(original_string))
    print(f"Found: {reparse_result} (len:{len(reparse_result)}).")

    assert reparse_result is not None
    for expected, result in zip_longest(expected_output, reparse_result):
        assert result == expected


def test_empty_token():
    """Test that empty tokens are correctly dropped."""

    assert sy.of_type(sy.EmptySemanticType)("", [], []) is None
