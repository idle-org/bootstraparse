# Dedicated module for the syntax of all the parsing
# All tokens inherit a SemanticType among SemanticType, ExplicitSemanticType and EmptySemanticType
# All tokens have a label, and __eq__ and __ne__ methods.
# Note: there is an UnimplementedToken
# Usage:
#   from bootstraparse.modules.syntax import line
#   line.parse_line('string') # returns a List of tokens
#   line_to_replace.parse_line('string') # returns a List of tokens parsed for replacements
#   imports.parse_line('string', True) # returns a List of tokens parsed for imports # FUTURE: Not implemented yet
#   any_token.create_diagram("filename") # Debugging

import os
from itertools import zip_longest
from collections import namedtuple

from bootstraparse.modules.error_mngr import MismatchedContainerError

import pyparsing as pp
import regex  # future: remove regex

pps = pp.Suppress


# Semantic group types
class SemanticType:
    """
    Allows us to access basic operations and identify each token parsed.
    """
    label = None

    def __init__(self, content):
        self.content = content

    def to_markup(self):
        """
        Function used for testing and readability purposes. Replaces matched markup with html-like tags.
        """
        if self.content:
            return_list = []
            for elt in self.content:
                try:
                    return_list.append(elt.to_markup())
                except Exception: # noqa E722 (This function is used for testing only)
                    return_list.append(str(elt))
            return f"<{self.label} = '{','.join(return_list)}' />"
        return f'<[NOC] {self.label} />'

    def __str__(self):
        if type(self.content) == str:
            return f'{self.label}[{self.content}]'
        else:
            return f'{self.label}{self.content}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if type(other) == type(self):
            for e1, e2 in zip_longest(self.content, other.content):
                if isinstance(e1, (pp.ParseResults, list)):  # if it's a list, we need to compare each element
                    for elt1, elt2 in zip_longest(e1, e2):
                        if elt1 != elt2:
                            return False
                elif e1 != e2:
                    return False
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def counterpart(self):  # noqa # FUTURE: Check for static counterpart implementation
        return None

    def to_container(self):
        """
        Function called by the context manager to know how to deal with the encapsulation of the token.
        Returns
        -------
            SemanticType
                Self if containable, the expected replacement token if it can, raises an error otherwise.
        Raises
        ------
            CannotBeContainedError
                Raises error if the token we were trying to encapsulate cannot be (probably mismatched).
        """
        raise MismatchedContainerError(self)


class AddFirstElementToLabel(SemanticType):
    def __init__(self, content):
        super().__init__(content)
        self.label += ":" + content[0]
        self._addendum = content[0]


class ExplicitSemanticType(SemanticType):
    """
    Explicit semantic type, the label is the only information we need.
    """
    def counterpart(self):
        return self.label

    def to_markup(self):
        return f'<{self.label} />'

    def to_container(self):
        return TextToken(self.content[0])


class FinalSemanticType(SemanticType):
    """
    Semantic type used by the context manager to ascertain token is possible to encapsulate.
    """

    def counterpart(self):  # noqa
        return None

    def to_container(self):
        return self


class OpenedSemanticType(SemanticType):
    """
    Semantic type used to signify it has a matching end component and needs to be matched.
    """
    def to_container(self):
        return self


class ClosedSemanticType(SemanticType):
    """
    Semantic type used to signify it has a matching start component and needs to be matched.
    """
    # def counterpart(self):
    #     return self.label[:-4]+'start'


class EmptySemanticType(FinalSemanticType):
    """
    Empty semantic type, the content is the only information we need.
    """
    def to_markup(self):
        if type(self.content) == str:
            return f'{self.content}'
        else:
            return " ".join(map(str, self.content))


class UnimplementedToken(SemanticType):
    label = "unimplemented"


class AliasToken(SemanticType):
    label = "alias"


class ImageToken(SemanticType):
    label = "image"


class TextToken(EmptySemanticType):
    label = "text"

    def to_container(self):
        return self


# FUTURE: all one-line elements should to inherit FinalSemanticType
class EnhancedToken(ExplicitSemanticType):
    """Mother of all EtTokens"""
    label = "text:enhanced"


class EtEmToken(ExplicitSemanticType):
    """*"""
    label = "text:em"


class EtStrongToken(ExplicitSemanticType):
    """**"""
    label = "text:strong"


class EtUnderlineToken(ExplicitSemanticType):
    """__"""
    label = "text:underline"


class EtStrikethroughToken(ExplicitSemanticType):
    """~~"""
    label = "text:strikethrough"


class EtCustomSpanToken(SemanticType):
    """(#int)"""
    label = "text:custom_span"


class EtUlistToken(FinalSemanticType):
    """-"""
    label = "list:ulist"


class EtOlistToken(FinalSemanticType):
    """#."""
    label = "list:olist"


class HeaderToken(FinalSemanticType):
    """
    # string #
    number of # indicates level
    """
    label = "header"


class DisplayToken(FinalSemanticType):
    """
    ! string !
    number of ! indicates level
    """
    label = "display"


class StructuralElementStartToken(AddFirstElementToLabel, OpenedSemanticType):
    """<<div|article|section|aside"""
    label = 'se:start'


class StructuralElementEndToken(AddFirstElementToLabel, ClosedSemanticType):
    """div|article|section|aside>>"""
    label = "se:end"

    def counterpart(self):
        return f"se:start:{self._addendum}"


class HyperlinkToken(SemanticType):
    label = "hyperlink"


class TableToken(SemanticType):
    label = "table"


class TableRowToken(SemanticType):
    label = "table:row"


class TableCellToken(SemanticType):
    label = "table:cell"


class TableSeparatorToken(SemanticType):
    label = "table:separator"


class OptionalToken(SemanticType):
    label = "optional"


class OptionalInsertToken(SemanticType):
    label = "optional:insert"


class OptionalVarToken(SemanticType):
    label = "optional:var"


class OptionalClassToken(SemanticType):
    label = "optional:class"


class BeAssignToken(SemanticType):
    label = "be:assign"


class BeValueToken(SemanticType):
    label = "be:var"


class BlockQuoteToken(SemanticType):
    label = "bq:text"


class BlockQuoteAuthorToken(SemanticType):
    label = "bq:author"


class Linebreak(ExplicitSemanticType):
    label = "linebreak"

    def to_container(self):
        return self


def of_type(token_class):
    """
    Function creating a custom function for generating the given Token type.
    :param token_class: SemanticType class
    :return: returns a function creating an instance of the given class
    """
    def _of_type(_, __, content):
        if len(content) == 0:  # Drop Empty token
            return None
        return token_class(content)

    return _of_type


def reparse(parse_element):
    """
    Creates a function which re-parses given match with specified parsing element.
    :param parse_element: pp object defining desired match
    :return: returns a function parsing given match with specified parsing element
    """
    def _reparse(__, _, tokens):
        return parse_element.parseString(tokens[0])  # Future: fix this with a proper solution

    return _reparse


"""
Tuple for readabilty of attributes over other modules.
"""
SplitOptionals = namedtuple(
    "SplitOptionals", ['html_insert', 'class_insert', 'var_list', 'var_dict'], defaults=['', '', [], {}]
)


def split_optionals(optionals):
    var_list = []
    var_dict = {}
    ci = ''
    hi = ''
    if not optionals:
        return SplitOptionals()
    for element in optionals.content:
        if element.label == 'optional:class':
            ci += " " + element.content[0]
        elif element.label == 'optional:insert':
            hi += " " + element.content[0]
        elif element.label == 'optional:var':
            for e in element.content.var:
                if e.label == 'be:var':
                    var_list.append(e.content.value[0])
                elif e.label == 'be:assign':
                    var_dict[e.content.assignation.var_name] = e.content.assignation.var_value[0]
    return SplitOptionals(html_insert=hi[1:], class_insert=ci[1:], var_list=var_list, var_dict=var_dict)


def readable_markup(list_of_tokens):
    """
    Function used for testing and readability purposes. Replaces matched markup with html-like tags.
    :param list_of_tokens: list of matched markup tokens in analysed text.
    :return: returns readable string.
    :rtype: string
    """
    readable_list = []
    for token in list_of_tokens:
        if type(token) == str:
            readable_list.append(token)
        else:
            try:
                readable_list.append(token.to_markup())
            except Exception: # noqa E722 (This function is used for testing and readability purposes)
                readable_list.append(str(token))
    return " ".join(readable_list)


# Pre-parser expressions
rgx_import_file = regex.compile(r'::( ?\< ?(?P<file_name>[\w\-._/]+) ?\>[ \s]*)+')


# Base elements
quotes = pp.Word(r""""'""")
value = (pps(quotes) + pp.Word(pp.alphanums + r'\._') + pps(pp.match_previous_literal(quotes)) ^
         pp.common.number ^ pp.common.fnumber)("value")
assignation = pp.Group(
    pp.common.identifier('var_name') + pps('=') + value('var_value')
)("assignation")
text = pp.OneOrMore(pp.Word(pp.alphanums))('text').add_parse_action(of_type(TextToken))
url_characters = pp.common.url

# Composite elements
var = pps('[') + pp.delimitedList(
    assignation.add_parse_action(of_type(BeAssignToken)) ^
    value.add_parse_action(of_type(BeValueToken))
)("list_vars").set_name("list_vars") + pps(']')

# Specific elements
image_element = ('@{' + pp.SkipTo('}')('image_name') + '}')("image_element")
alias_element = ('@[' + pp.SkipTo(']')('alias_name') + ']')("alias_element")
expression = pp.Word(pp.alphanums + r'=+-_\'",;:!\/\\. ')
html_insert = pps('{') + expression('html_insert') + pps('}')
class_insert = pps('{{') + expression('class_insert') + pps('}}')

# Optional elements
optional = pp.OneOrMore(
        class_insert("class_insert").add_parse_action(of_type(OptionalClassToken)) ^
        html_insert("html_insert").add_parse_action(of_type(OptionalInsertToken)) ^
        var("var").add_parse_action(of_type(OptionalVarToken))
)("optional").add_parse_action(of_type(OptionalToken))  # Macro OptionalToken

# Structural elements
structural_elements = (
        pp.CaselessLiteral('div') |
        pp.CaselessLiteral('article') |
        pp.CaselessLiteral('aside') |
        pp.CaselessLiteral('section')
)('structural_element')
header_element = pp.Word('#')
display_element = pp.Word('!')

# Inline elements
il_link = pp.Regex(
    r"""\[(?P<text>.+)\]\(['"]?(?P<url>[a-zA-Z-_:\/=@#!%\?\d\(\)\.]+)['"]?\)"""
).add_parse_action(of_type(HyperlinkToken))

# Enhanced text elements
et_em = pp.Literal('*')('em').add_parse_action(of_type(EtEmToken))
et_strong = pp.Literal('**')('strong').add_parse_action(of_type(EtStrongToken))
et_underline = pp.Literal('__')('underline').add_parse_action(of_type(EtUnderlineToken))
et_strikethrough = pp.Literal('~~')('strikethrough').add_parse_action(of_type(EtStrikethroughToken))
et_custom_span = (
        pps('(#') + pp.Word(pp.nums)('span_id') + pps(')')
).set_name('custom_span').add_parse_action(of_type(EtCustomSpanToken))

# markup sums up all in-line elements
markup = il_link | et_strong | et_em | et_strikethrough | et_underline | et_custom_span
enhanced_text = pp.ZeroOrMore(
    markup | pp.SkipTo(markup)('text').add_parse_action(of_type(TextToken)) + markup
) + pp.Opt(pp.Regex(r'.+')("text").add_parse_action(of_type(TextToken)))

# Multiline elements
se_start = (pps('<<') + structural_elements).add_parse_action(of_type(StructuralElementStartToken))
se_end = (structural_elements + pps('>>')).add_parse_action(of_type(StructuralElementEndToken)) + pp.Opt(optional)
se = se_end | se_start  # Structural element
table_row = pp.OneOrMore(
        # pp.Regex(r'\|(\d)?')('table_colspan') +
        (pp.Combine(pps('|') + pp.Word(pp.nums)('table_colspan')) | pps('|')) +
        pp.SkipTo('|')('table_cell').add_parse_action(reparse(enhanced_text), of_type(TableCellToken))
).add_parse_action(of_type(TableRowToken)) + pps('|') + pp.Opt(optional)
table_separator = pp.OneOrMore(
    pps('|') + pp.Word(':-')
)('table_separator').add_parse_action(of_type(TableSeparatorToken)) + pps('|')
# Future: Add Blockquote element
blockquote = pps(pp.Literal('>')) + \
             pp.SkipTo(pp.line_end)('text').add_parse_action(reparse(enhanced_text), of_type(BlockQuoteToken))
blockquote_author = pps(pp.Literal('> --')) + \
                    pp.SkipTo(pp.line_end)('author').add_parse_action(of_type(BlockQuoteAuthorToken))
table = table_separator | table_row
quotation = blockquote_author | blockquote

# multi_line sums up all multi-line elements
multi_line = se | table | quotation

# Oneline elements
one_header = (
        header_element +
        pp.SkipTo(pp.match_previous_literal(header_element)) +
        pps(pp.match_previous_literal(header_element)) +
        pp.Opt(optional)
).add_parse_action(of_type(HeaderToken))
one_display = (
        display_element +
        pp.SkipTo(pp.match_previous_literal(display_element)) +
        pps(pp.match_previous_literal(display_element)) +
        pp.Opt(optional)
).add_parse_action(of_type(DisplayToken))
one_olist = pp.line_start + (
        pps(pp.Literal('#.')) + (
         (pp.SkipTo(optional)('text').add_parse_action(reparse(enhanced_text)) + optional) |
         enhanced_text)
).add_parse_action(of_type(EtOlistToken))
one_ulist = pp.line_start + (
        pps(pp.Literal('-')) + (
         (pp.SkipTo(optional)('text').add_parse_action(reparse(enhanced_text)) + optional) |
         enhanced_text)
).add_parse_action(of_type(EtUlistToken))

# one_line sums up all one-line elements
one_line = (one_header | one_display | one_olist | one_ulist)

# Final elements
line = one_line | multi_line | enhanced_text


##############################################################################
# Pre_parser elements
##############################################################################

# Composite elements
image = image_element + pp.Opt(optional)
alias = alias_element + pp.Opt(optional)

# Syntax elements
line_to_replace = pp.OneOrMore(
    pp.SkipTo(image ^ alias)('text').add_parse_action(of_type(TextToken))
    ^ image.add_parse_action(of_type(ImageToken))
    ^ alias.add_parse_action(of_type(AliasToken))
) ^ pp.rest_of_line('text').add_parse_action(of_type(TextToken))


##############################################################################
# Temporary tests
##############################################################################
if __name__ == '__main__':  # pragma: no cover
    pp.autoname_elements()

    if not os.path.exists('../../../dev_outputs/'):
        os.mkdir('../../../dev_outputs/')
    line.create_diagram("../../../dev_outputs/diagram_line.html")
    multi_line.create_diagram("../../../dev_outputs/diagram_multi_line.html")
    one_line.create_diagram("../../../dev_outputs/diagram_one_line.html")
    enhanced_text.create_diagram("../../../dev_outputs/diagram_enhanced_text.html")
