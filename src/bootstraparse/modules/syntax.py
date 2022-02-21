# Dedicated module for the syntax of all the parsing
import pyparsing as pp
import rich

pps = pp.Suppress

# base elements
value = pps('"') + pp.Word(pp.alphanums + r'.') + pps('"') ^ pps("'") + pp.Word(pp.alphanums + r'.') + pps("'") ^ pp.common.fnumber
assignation = pp.Group(pp.common.identifier('var_name') + '=' + value('var_value'))

# composite elements
var = '[' + pp.Group(assignation + pp.ZeroOrMore(pp.Suppress(r',') + assignation))('vars') + ']'

# specific elements
image_element = '@{' + pp.common.identifier('image_name') + '}'
alias_element = '@[' + pp.common.identifier('alias_name') + ']'
expression = pp.Word(pp.alphanums + r'=+-_\'",;: ')
html_insert = '{' + expression('html_insert') + '}'


# preparer elements
image = image_element + html_insert + var
alias = alias_element + html_insert + var

# syntax elements

###############################################################################
# Temporary tests
if __name__ == '__main__':  # pragma: no cover
    test_string = r'@[custom_pict]{class="watabuya"}[number="2", _important=22, touze=12]'

    saucisse = alias.parse_string(test_string)
    # rich.inspect(final.parse_string(test_string))
    rich.inspect(saucisse)

    for e in saucisse.vars:
        print(f'{e.var_name} equals "{e.var_value}"')
