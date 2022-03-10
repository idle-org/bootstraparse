# Dedicated module for the syntax of all the parsing
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
            return f'{self.label}[{self.content}]'

    def __repr__(self):
        return str(self)


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

# Composite elements
var = '[' + pp.delimitedList(assignation ^ value)("list_vars").set_name("list_vars") + ']'

# Enhanced text
enhanced_text = pp.Forward()
et_em = (pps('*') + enhanced_text + pps('*'))('em').add_parse_action(of_type(EtEmToken))
et_strong = (pps('**') + enhanced_text + pps('**'))('strong').add_parse_action(of_type(EtStrongToken))
et_underline = (pps('__') + enhanced_text + pps('__'))('underline').add_parse_action(of_type(EtUnderlineToken))
et_strikethrough = (pps('~~') + enhanced_text + pps('~~'))('strikethrough').add_parse_action(of_type(EtStrikethroughToken))
custom_span = ('(#' + pp.Word(pp.nums)('span_id') + ')').set_name('span_tag')
et_custom_span = \
    (custom_span + enhanced_text + pp.match_previous_literal(custom_span))('custom_span')\
    .add_parse_action(of_type(EtCustomSpanToken))
enhanced_text <<= (text | et_strong | et_em | et_underline | et_strikethrough | et_custom_span) + pp.Opt(enhanced_text)


# Specific elements
image_element = ('@{' + pp.common.identifier('image_name') + '}')("image_element")
alias_element = ('@[' + pp.common.identifier('alias_name') + ']')("alias_element")
expression = pp.Word(pp.alphanums + r'=+-_\'",;: ')
html_insert = '{' + expression('html_insert') + '}'

# Optional elements
optional = (pp.Opt(html_insert)("html_insert") + pp.Opt(var)("var"))("optional")

# Preparser elements
image = image_element + optional
alias = alias_element + optional

# Syntax elements
line_to_replace = pp.OneOrMore(pp.SkipTo(image ^ alias)('text').add_parse_action(of_type(TextToken)) ^
                               image.add_parse_action(of_type(ImageToken)) ^
                               alias.add_parse_action(of_type(AliasToken)))\
                  ^ pp.SkipTo(pp.lineEnd)('text').add_parse_action(of_type(TextToken))

###############################################################################
# Temporary tests
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
    ]
    enhanced_text.create_diagram("../../../dev_outputs/diagram.html")
    for string in list_strings:
        print('Input string:', string)
        output = enhanced_text.parseString(string)
        # rich.inspect(output)
        print('Output string:', readable_markup(output))
        print()
