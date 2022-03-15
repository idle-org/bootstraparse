import pyparsing
import pytest

import bootstraparse.modules.syntax as sy

# Dictionary of all label and associated token used in the Pre_parser
list_of_token_types = {
    "alias": sy.AliasToken,
    "image": sy.ImageToken,
}

# Dictionary of all lexical elements and a list of matching strings for the Pre_parser
expressions_to_match = {
    # Base elements
    "quotes": ["'hi, there'", "'hi, there'"],
    "value": ["0.1", "'hello'"],
    "assignation": ["a=1", "a=1.33", "tr2='hu'"],

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
    "optional": ["a=1", "a=1.33", "tr2='hu'"],

    # Pre_parser elements
    "image": ["@{image}{test=22}[a=12,22,c,d,ERE,r,3]", "@{image123_456}{a=12,22,c,d,ERE,r,3}",
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

# Testing the parser lexical elements
dict_advanced_syntax_input_and_expected_output = {
    # Enhanced text # TODO : Test optional inline args
    "et_em": [
        # Single em element, should only match the first "*"
        ("*", (sy.EtEmToken("*"), )),
    ],
    "et_strong": [
        # Single strong element, should only match the first "**"
        ("**", sy.EtEmToken("**"), ),
    ],
    "et_underline": [
        # Single underline element, should only match the first "__"
        ("__", (sy.EtUnderlineToken("__"), )),
    ],
    "et_strikethrough": [
        # Single strikethrough element, should only match the first "~~"
        ("~~", (sy.EtStrikethroughToken("~~"), )),
    ],
    "et_custom_span": [
        # Single custom span element, should only match the first "(#number)"
        ("(#12345)", (sy.EtCustomSpanToken("#12345"), )),
    ],
    "il_link": [
        # Single link element, should only match the first "[link_name](link)"
        # TODO: Text tokens ? or Link token and hyperlink token ?
        ("[text_link]('text://www.website.com/link.html')",
         sy.HyperlinkToken("[text_link]('text://www.website.com/link.html')"))
    ],

    # Enhanced Text
    "enhanced_text": [
        # Matches a line of text, with or without inline elements
        ("*test*", (sy.EtEmToken(["*"]), sy.TextToken(["test"]), sy.EtEmToken(["*"]))),
        ("**test**", (sy.EtEmToken(["**"]), sy.TextToken(["test"]), sy.EtEmToken(["**"]))),
        ("__test__", (sy.EtUnderlineToken(["__"]), sy.TextToken(["test"]), sy.EtUnderlineToken(["__"]))),
        ("~~test~~", (sy.EtStrikethroughToken(["~~"]), sy.TextToken(["test"]), sy.EtStrikethroughToken(["~~"]))),
        ("(#12345)", (sy.EtCustomSpanToken(["#12345"]), )),
        ("*test*test*", (sy.EtEmToken(["*"]), sy.TextToken(["test"]), sy.EtEmToken(["*"]), sy.TextToken(["test"]),
                         sy.EtEmToken(["*"]))),
        ("**test**test**", (sy.EtEmToken(["**"]), sy.TextToken(["test"]), sy.EtEmToken(["**"]), sy.TextToken(["test"]),
                            sy.EtEmToken(["**"]), )),
        ("__test__test__", (sy.EtUnderlineToken(["__"]), sy.TextToken(["test"]), sy.EtUnderlineToken(["__"]),
                            sy.TextToken(["test"]), sy.EtUnderlineToken(["__"]), )),
        ("~~test~~test~~", (sy.EtStrikethroughToken(["~~"]), sy.TextToken(["test"]), sy.EtStrikethroughToken(["~~"]),
                            sy.TextToken(["test"]), sy.EtStrikethroughToken(["~~"]), )),
        ("(#12345)test(#12345)", (sy.EtCustomSpanToken(["#12345"]), sy.TextToken(["test"]),
                                  sy.EtCustomSpanToken(["#12345"]), )),
        ("__test(#12)test**test__test~~", (sy.EtUnderlineToken("__"), sy.TextToken(["test"]),
                                           sy.EtCustomSpanToken(["#12"]), sy.TextToken(["test"]), sy.EtEmToken(["**"]),
                                           sy.TextToken(["test"]), sy.EtStrikethroughToken(["~~"]),
                                           sy.TextToken(["test"]), sy.EtUnderlineToken(["__"]), )),
        ("12. List", (sy.EtUlistToken(["12."]), sy.TextToken([" List"]), )),
        ("Test text with a link [link_name](link)", (sy.TextToken(["Test text with a link "]),
                                                     sy.HyperlinkToken(["link_name", "link"]), )),
        ("Test text with a link [link_name](link) and a *bold* text", (sy.TextToken(["Test text with a link "]),
                                                                       sy.HyperlinkToken(["link_name", "link"]),
                                                                       sy.TextToken([" and a "]), sy.EtEmToken(["*"]),
                                                                       sy.TextToken(["bold"]), sy.EtEmToken(["*"]), )),
    ],

    # Divs
    "et_div": [
        # Matches a div element, must be at the beginning of the line, the closing div can be with arguments
        # TODO: Implement a specific div token
        ("<<div", (sy.UnimplementedToken(["<<", "div"]), )),
        ("div>>", (sy.UnimplementedToken(["div", ">>"]))),
        # TODO: Add a specific optional token for the arguments
        ("div>> [class='blue', 123#]{var='test', number=11}", (sy.UnimplementedToken(["div", ">>", sy.UnimplementedToken(["[", "class='blue'", ",", "123#", "]"]), sy.UnimplementedToken(["{", "var='test'", ",", "number=11", "}"])]))), # noqa E501 (line too long)
    ],

    # Elements
    "one_olist": [
        # Matches a one-level ordered list element, must be at the beginning of the line
        # Drop the "." from the match
        ("12. Text", (sy.EtOlistToken(["12", sy.TextToken(["Text"])]), )),
    ],
    "one_ulist": [
        # Matches a one-level unordered list element, must be at the beginning of the line
        # Drop the "-" from the match
        ("- Text", [sy.EtUlistToken([sy.TextToken(["Text"])]), ]),
    ],

    # Headers
    "one_header": [
        # Matches a one-level header element, must be at the beginning of the line
        ("# Text1 #", (sy.HeaderToken(["#", "Text1"]), )),
        ("## Text2 ##", (sy.HeaderToken(["##", "Text2"]), )),
        ("### Text3 ###", (sy.HeaderToken(["###", "Text3"]), )),
        ("#### Text4 ####", (sy.HeaderToken(["####", "Text4"]), )),
        ("##### Text5 #####", (sy.HeaderToken(["#####", "Text5"]), )),
        ("###### Text6 ######", (sy.HeaderToken(["######", "Text6"]), )),
        ("## Text2 ## {var='test', number=11}", (sy.HeaderToken(["##", "Text2"]),
                                                 sy.UnimplementedToken(["{", "var='test'", ",", "number=11", "}"]))),
        ("### Text3 ### [class='blue', 123#]{var='test', number=11}", (sy.HeaderToken(["###", "Text3"]),
                                                                       sy.UnimplementedToken(["[", "class='blue'", ",", "123#", "]"]), # noqa E501 (line too long)
                                                                       sy.UnimplementedToken(["{", "var='test'", ",", "number=11", "}"]))), # noqa E501 (line too long)
    ],
    # Tables
    "table_row": [
        # Matches a table element, must be at the beginning of the line # TODO: add TableCellToken?
        ("| Text1 | Text2 |", (sy.TableRowToken(["|", "Text1", "|", "Text2", "|"]), )),
        ("| Text1 | Text2 | Text3 |", (sy.TableRowToken(["|", "Text1", "|", "Text2", "|", "Text3", "|"]), )),
        ("|2 Text1 | Text2 |", (sy.TableRowToken(["|2", "Text1", "|", "Text2", "|"]), )),
        ("|2 Text1 |3 Text2 |", (sy.TableRowToken(["|2", "Text1", "|3", "Text2", "|"]), )),
        ("|2 Text1 |3 Text2 |4 Text3 |", (sy.TableRowToken(["|2", "Text1", "|3", "Text2", "|4", "Text3", "|"]), )),
        ("|3 Text1 | Text2 | {var='test', number=11}", (sy.TableRowToken(["|3", "Text1", "|", "Text2", "|"]), sy.UnimplementedToken(["{", "var='test'", ",", "number=11", "}"]))), # noqa E501 (line too long)
    ],
    "table_separator": [
        # Matches a table element, must be at the beginning of the line # TODO: Tokens ?
        ("|---|---|", (sy.TableSeparatorToken(["|", "---", "|", "---", "|"]), )),
        ("|---|---|---|", (sy.TableSeparatorToken(["|", "---", "|", "---", "|", "---", "|"]), )),
        ("|:--|-:-|--:|--:|", (sy.TableSeparatorToken(["|", ":--", "|", "-:-", "|", "--:", "|", "--:", "|"]), )),
    ],
    "line": [
        # Match any line parsed by the parser (can match header, list table etc...) this is the main syntax element
        ("# Text1 #", (sy.HeaderToken(["#", "Text1"]), )),
        ("Text *bold __underline__ still bold*", (sy.TextToken(["Text ", sy.EtStrongToken(["bold", " ", sy.EtUnderlineToken(["underline"]), " still bold"])]), )),  # noqa E501 (line too long)
        ("|2 Text1 | Text2 |", (sy.TableRowToken(["|2", "Text1", "|", "Text2", "|"]), )),
        ("|---|---|", (sy.TableSeparatorToken(["|", "---", "|", "---", "|"]), )),
        ("- Text", (sy.EtUlistToken([sy.TextToken(["Text"])]), )),
        ("div>>", (sy.UnimplementedToken(["div", ">>"]), )),
    ],
}


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
    tnk = fcr(None, None, None)
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


@pytest.mark.xfail(reason="Not implemented yet.")
@pytest.mark.parametrize("expression, tokens", dict_advanced_syntax_input_and_expected_output.items())
def test_advanced_expression_and_token_creation(expression, tokens):
    """
    Test that the advanced syntax is correctly parsed and returns the correct tokens.
    :param expression: The expression to test.
    :param tokens: The expected tokens.
    :type expression: str
    :type tokens: list
    """
    expr = find_expression_from_str(expression)

    assert isinstance(expr, pyparsing.ParserElement)
    for string_to_test, expected_tokens in tokens:
        result = expr.parse_string(string_to_test)
        print("Found:", result, "Expected:", expected_tokens)
        assert result is not None
        for token, expected_token in zip(result, expected_tokens):
            assert token == expected_token
