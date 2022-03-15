# Dedicated module for the syntax of all the parsing
import os
import pyparsing as pp
import rich

pps = pp.Suppress


# Semantic group types
class SemanticType:
    """
    Allows us to access basic operations and identify each token parsed.
    """
    label = None

    def __init__(self, content):
        self.content = content

    def __str__(self):
        if type(self.content) == str:
            return f'{self.label}[{self.content}]'
        else:
            return f'{self.label}{self.content}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if type(other) == type(self):
            for e1, e2 in zip(self.content, other.content):
                if e1 != e2:
                    return False
            return True
        return False


class UnimplementedToken(SemanticType):
    label = "unimplemented"


class AliasToken(SemanticType):
    label = "alias"


class ImageToken(SemanticType):
    label = "image"


class TextToken(SemanticType):
    label = "text"


class EnhancedToken(SemanticType):
    label = "text:enhanced"


class EtEmToken(SemanticType):
    label = "text:em"


class EtStrongToken(SemanticType):
    label = "text:strong"


class EtUnderlineToken(SemanticType):
    label = "text:underline"


class EtStrikethroughToken(SemanticType):
    label = "text:strikethrough"


class EtCustomSpanToken(SemanticType):
    label = "text:custom_span"


class EtUlistToken(SemanticType):
    label = "list:ulist"


class EtOlistToken(SemanticType):
    label = "list:olist"


class HeaderToken(SemanticType):
    label = "header"


class StructuralElementStartToken(SemanticType):
    label = "se:start"


class StructuralElementEndToken(SemanticType):
    label = "se:end"


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


def of_type(token_class):
    """
    Function creating a custom function for generating the given Token type.
    :param token_class: SemanticType class
    :return: returns a function creating an instance of the given class
    """
    def _of_type(_, __, content):
        return token_class(content)

    return _of_type


def readable_markup(list_of_tokens):
    """
    Function used for testing and readability purposes. Replaces matched markup with html-like tags.
    :param list_of_tokens: list of matched markup tokens in analysed text.
    :return: returns readable string.
    :rtype: string
    """
    readable_string = ''
    for token in list_of_tokens:
        if type(token) == str:
            readable_string += token
        elif token.label == 'text:em':
            readable_string += _add_tag('em', readable_markup(token.content))
        elif token.label == 'text:strong':
            readable_string += _add_tag('b', readable_markup(token.content))
        elif token.label == 'text:underline':
            readable_string += _add_tag('u', readable_markup(token.content))
        elif token.label == 'text:strikethrough':
            readable_string += _add_tag('st', readable_markup(token.content))
        elif token.label == 'text:custom_span':
            readable_string += _add_tag('#', readable_markup(token.content))
        elif token.label == 'text':
            readable_string += ' ' + ' '.join(token.content)
        else:
            raise Exception('Unknown token type' + token.label)
    return readable_string[1:]


def _add_tag(tag, content):
    if content:
        return f' <{tag}>{content}</{tag}>'
    return ''


# create_image_token = of_type(ImageToken)
# create_image_token()

# Base elements
quotes = pp.Word(r""""'""")
value = (quotes + pp.Word(pp.alphanums + r'.') + pp.match_previous_literal(quotes) ^
         pp.common.fnumber)("value")
assignation = pp.Group(pp.common.identifier('var_name') + '=' + value('var_value'))("assignation")
text = pp.OneOrMore(pp.Word(pp.alphanums))('text').add_parse_action(of_type(TextToken))
http_characters = pp.Word(pp.alphanums + r'=+-_\/\\.:;!?%#@&*()[]{}~` ')  # Todo : Check common.url that can match any common url structure # noqa E501 # pylint: disable=line-too-long

# Composite elements
var = '[' + pp.delimitedList(assignation ^ value)("list_vars").set_name("list_vars") + ']'


# Specific elements
image_element = ('@{' + pp.common.identifier('image_name') + '}')("image_element")
alias_element = ('@[' + pp.common.identifier('alias_name') + ']')("alias_element")
expression = pp.Word(pp.alphanums + r'=+-_\'",;:!<> ')
html_insert = '{' + expression('html_insert') + '}'
structural_elements = \
    (pp.Word('div') ^ pp.Word('article') ^ pp.Word('aside') ^ pp.Word('section'))('structural_element') # TODO : Fixit: Word is "make a word with any of the characters in the string" whereas Literal is "make a word with a specific string" # noqa E501 (line too long)


# Optional elements
optional = (pp.Opt(html_insert)("html_insert") + pp.Opt(var)("var"))("optional") # TODO : Make an optional token ? and maybe a htmlInsertToken and a varToken # noqa E501 (line too long)

# TODO :
#  Everywhere : Avoid text at all costs since it is not a valid token, make a new token for it or use pp.SkipTo or (...)
# Enhanced text elements # TODO: Add all markups so that they can be parsed, they no longer need to be linked
# et_em = ('*' + enhanced_text + '*')('em').add_parse_action(of_type(EtEmToken))
# et_strong = ('**' + enhanced_text + '**')('strong').add_parse_action(of_type(EtStrongToken))
# et_underline = ('__' + enhanced_text + '__')('underline').add_parse_action(of_type(EtUnderlineToken))
# et_strikethrough = ('~~' + enhanced_text + '~~')('strikethrough').add_parse_action(of_type(EtStrikethroughToken))
# custom_span = ('(#' + pp.Word(pp.nums)('span_id') + ')').set_name('span_tag')
# et_custom_span = \
#     (custom_span + enhanced_text + pp.match_previous_literal(custom_span))('custom_span')\
#     .add_parse_action(of_type(EtCustomSpanToken))
# enhanced_text <== (text | et_strong | et_em | et_underline |
# et_strikethrough | et_custom_span) + pp.Opt(enhanced_text)

# Multiline elements
# TODO: We decided for << instead of ~~ because it is easier to parse
se_start = ('~~' + structural_elements).add_parse_action(of_type(StructuralElementStartToken))
se_end = (structural_elements + '~~').add_parse_action(of_type(StructuralElementEndToken))
se = se_end | se_start  # Structural element # TODO Check nomenclature

# Inline elements
il_link = pp.Literal('[') + ... + pp.Literal('](') + pp.QuotedString("'\"", esc_char='\\') + ')'

# Oneline elements
# TODO: one_header should match any number of '#' I suggest either a div_element=Word("#") or a div_element=OneOrMore(pp.Literal('#')) with a pp.match_previous_literal(dive=_element) # noqa E501 (line too long)
one_header = (pp.Literal('#') + ... + pps(" "+'#')).add_parse_action(of_type(HeaderToken))

# TODO: Don't use "^" (longest match wins) use "|" (first match wins) # TODO: add a ("name") ? # TODO: Suppress the "."
one_olist = pp.line_start + \
            ((pp.Word(pp.nums) ^ pp.Word('#')) + '.' + ... + pp.line_end).add_parse_action(of_type(EtOlistToken))

# TODO: add a ("name") ?
one_ulist = pp.line_start + \
            (pp.Literal('-') + ... + pp.line_end).add_parse_action(of_type(EtUlistToken))

# Final elements
enhanced_text = text  # TODO: It's actually text or et_em or et_strong etc..., either recursive or repeated


##############################################################################
# Pre_parser elements
##############################################################################

# Composite elements
image = image_element + optional
alias = alias_element + optional

# Syntax elements
line_to_replace = pp.OneOrMore(pp.SkipTo(image ^ alias)('text').add_parse_action(of_type(TextToken)) ^
                               image.add_parse_action(of_type(ImageToken)) ^
                               alias.add_parse_action(of_type(AliasToken)))\
                  ^ pp.SkipTo(pp.lineEnd)('text').add_parse_action(of_type(TextToken))

##############################################################################
# Temporary tests
##############################################################################
if __name__ == '__main__':  # pragma: no cover
    pp.autoname_elements()

    list_strings = [
        "Normal text",
        "Normal text *em text*",
        "Normal text **strong text**",
        "Normal text __underline text__",
        "Normal text ~~strikethrough text~~",
        "Normal text (#123) custom span text(#123)",
        "**Strong text __underline__** normal text",
        "Normal text **strong text *em text*** *em text **strong text*** normal text",
        "<<div",
        "div>>",
        "[link text]('http://test.icule')",
        "# header #",
        "1. ordered list",
        "- unordered list",
    ]
    # div_start.parse_string(list_strings[8])
    # div_end.parse_string(list_strings[9])
    # il_link.parse_string(list_strings[10])
    # one_header.parse_string(list_strings[11])
    # one_olist.parse_string(list_strings[12])
    # one_ulist.parse_string(list_strings[13])

    # enhanced_text.create_diagram("../../../dev_outputs/diagram.html")
    # for string in list_strings:
    #     print('Input string:', string)
    #     output = enhanced_text.parseString(string)
    #     # rich.inspect(output)
    #     print('Output string:', readable_markup(output))
    #     print()

    if not os.path.exists('../../../dev_outputs/'):
        os.mkdir('../../../dev_outputs/')
    enhanced_text.create_diagram("../../../dev_outputs/diagram.html")

    import timeit
    base_time = {}
    for string in list_strings:
        print('Input string:', string)
        n_time = timeit.timeit("enhanced_text.parseString(string)", number=100, globals=globals())
        base_time[string] = n_time
        output = enhanced_text.parseString(string)
        # rich.inspect(output)
        rich.print(f'[] Output string: {readable_markup(output)} in {n_time:.2}s)')
        print()

    time = timeit.timeit("enhanced_text.parseString(mega_string)", number=5, globals=globals())
    rich.print(f'[]Mega time: {time}')
    base_time['mega_string'] = time

    print('Base time:')
    for string, time in base_time.items():
        print(f'                 "{string}": {time},')
