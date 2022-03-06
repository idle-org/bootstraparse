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


def of_type(token_class):
    """
    Function creating a custom function for generating the given Token type.
    :param token_class: SemanticType class
    :return: returns a function creating an instance of the given class
    """
    def _of_type(_, __, content):
        return token_class(content)

    return _of_type


# create_image_token = of_type(ImageToken)
# create_image_token()
# Base elements
quotes = pp.Word(r""""'""")
value = (quotes + pp.Word(pp.alphanums + r'.') + pp.match_previous_literal(quotes) ^
         pp.common.fnumber)("value")
assignation = pp.Group(pp.common.identifier('var_name') + '=' + value('var_value'))("assignation")

# Composite elements
var = '[' + pp.delimitedList(assignation ^ value)("list_vars").set_name("list_vars") + ']'

# Specific elements
image_element = ('@{' + pp.common.identifier('image_name') + '}')("image_element")
alias_element = ('@[' + pp.common.identifier('alias_name') + ']')("alias_element")
expression = pp.Word(pp.alphanums + r'=+-_\'",;: ')
html_insert = '{' + expression('html_insert') + '}'

# Optional elements
optional = (pp.Opt(html_insert) + pp.Opt(var))("optional")

# Preparser elements
image = image_element + optional
alias = alias_element + optional

# Syntax elements
line_to_replace = image.add_parse_action(of_type(ImageToken)) ^ alias.add_parse_action(of_type(AliasToken))

###############################################################################
# Temporary tests
if __name__ == '__main__':  # pragma: no cover
    pp.autoname_elements()
    test_string = r"""@{custom_pict}{class='123watabuya'}[number="2", _important=22, touze=12]"""

    saucisse = line_to_replace.parse_string(test_string)
    rich.inspect(saucisse[0])
    line_to_replace.create_diagram("../../../tests/diagram.html")
