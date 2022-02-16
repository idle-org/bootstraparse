# Dedicated module for the syntax of all the parsing

import pyparsing as pp
import rich


image_parser = '@{' + pp.common.identifier('image_name') + '}'
expression_parser = pp.Word(pp.alphanums + r'=+_\'",')
class_parser = '{' + expression_parser('html_insert') + '}'
value_parser = pp.Word(pp.alphanums + r'\'"')
assignation = pp.Group(pp.common.identifier('var_name') + '=' + value_parser('var_value'))
var_parser = '[' + pp.Group(assignation + pp.ZeroOrMore(pp.Suppress(r',') + assignation))('vars') + ']'
final_parser = image_parser + class_parser + var_parser
test_string = r'@{custom_pict}{class="watabuya"}[number=2, _important=22, touze=12]'

saucisse = final_parser.parse_string(test_string)
# rich.inspect(final_parser.parse_string(test_string))
rich.inspect(saucisse.vars)

for e in saucisse.vars:
    print(e.var_name + ' equals ' + e.var_value)
