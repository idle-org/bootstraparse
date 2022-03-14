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
            return f'{self.label}[{self.content}]'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.content == other.content
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
http_characters = pp.Word(pp.alphanums + r'=+-_\/\\.:;!?%#@&*()[]{}~` ')

# Composite elements
var = '[' + pp.delimitedList(assignation ^ value)("list_vars").set_name("list_vars") + ']'

# Enhanced text # TODO: Add all markups so that they can be parsed
enhanced_text = None
# et_em = ('*' + enhanced_text + '*')('em').add_parse_action(of_type(EtEmToken))
# et_strong = ('**' + enhanced_text + '**')('strong').add_parse_action(of_type(EtStrongToken))
# et_underline = ('__' + enhanced_text + '__')('underline').add_parse_action(of_type(EtUnderlineToken))
# et_strikethrough = ('~~' + enhanced_text + '~~')('strikethrough').add_parse_action(of_type(EtStrikethroughToken))
# custom_span = ('(#' + pp.Word(pp.nums)('span_id') + ')').set_name('span_tag')
# et_custom_span = \
#     (custom_span + enhanced_text + pp.match_previous_literal(custom_span))('custom_span')\
#     .add_parse_action(of_type(EtCustomSpanToken))
# enhanced_text <<= (text | et_strong | et_em | et_underline | et_strikethrough | et_custom_span) + pp.Opt(enhanced_text)

# Multiline elements
div_start = '~~' + text  # TODO : It's not a text, rather a keyword and add ("name") et .add_parse_action(of_type(TextToken))
div_end = text + '~~'

# Inline elements
il_link = '[' + text + ']' + '(' + quotes + http_characters + pp.match_previous_literal(quotes) + ')'  # Todo: change the quotes to quotedstring, get rid of text which was a placeholder

# Oneline elements
one_header = '#' + text + '#'  # 1 per hX or copy paste six times?  # TODO: add a header level to the token and get rid of the text which was a placeholder
one_olist = pp.line_start + (pp.Word(pp.nums) ^ pp.Word('#')) + '.' + text  # TODO: add a ("name") and add .add_parse_action(of_type(TextToken))
one_ulist = pp.line_start + '-' + text  # TODO: add a ("name") and add .add_parse_action(of_type(TextToken)) and get rid of the text which was a placeholder

# Specific elements
image_element = ('@{' + pp.common.identifier('image_name') + '}')("image_element")
alias_element = ('@[' + pp.common.identifier('alias_name') + ']')("alias_element")
expression = pp.Word(pp.alphanums + r'=+-_\'",;:!<> ')
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

    def find_color(new_time, old_time):
        pct = percent(new_time, old_time)
        if pct < 80:
            return "red"
        elif pct > 130:
            return "green"
        return "yellow"

    def percent(new_time, old_time):
        return round((old_time/new_time) * 100, 2)

    list_strings = [
        "Normal text",
        "Normal text *em text*",
        "Normal text **strong text**",
        "Normal text __underline text__",
        "Normal text ~~strikethrough text~~",
        "Normal text (#123) custom span text(#123)",
        "**Strong text __underline__** normal text",
        "Normal text **strong text *em text*** *em text **strong text*** normal text",
        "~~div",
        "div~~",
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

    nominal_t = {"Normal text": 0.005791999999999992,
                 "Normal text *em text*": 0.017378599999999966,
                 "Normal text **strong text**": 0.021291599999999966,
                 "Normal text __underline text__": 0.016918500000000003,
                 "Normal text ~~strikethrough text~~": 0.016525699999999977,
                 "Normal text (#123) custom span text(#123)": 0.04130879999999998,
                 "**Strong text __underline__** normal text": 0.05399810000000005,
                 "Normal text **strong text *em text*** *em text **strong text*** normal text": 0.35971580000000003,
                 "mega_string": 4.5726051000000005,
                 }
    if not os.path.exists('../../../dev_outputs/'):
        os.mkdir('../../../dev_outputs/')
    enhanced_text.create_diagram("../../../dev_outputs/diagram.html")

    import timeit
    base_time = {}
    for string, time in nominal_t.items():
        if string == "mega_string":
            continue
        print('Input string:', string)
        n_time = timeit.timeit("enhanced_text.parseString(string)", number=100, globals=globals())
        base_time[string] = n_time
        output = enhanced_text.parseString(string)
        # rich.inspect(output)
        color = find_color(n_time, time)
        perc = percent(n_time, time)
        rich.print(f'[{color}]Output string: {readable_markup(output)} in {n_time:.2}s vs {time:.2} ({perc} %)[/{color}]')
        print()

    mega_string = ' '.join(list_strings)

    time = timeit.timeit("enhanced_text.parseString(mega_string)", number=5, globals=globals())
    color = find_color(time, nominal_t['mega_string'])
    perc = percent(time, nominal_t['mega_string'])
    rich.print(f'[{color}]Mega time: {time} vs {nominal_t["mega_string"]} ({perc})% [/{color}]')
    base_time['mega_string'] = time

    print('Base time:')
    for string, time in base_time.items():
        print(f'                 "{string}": {time},')
