from io import StringIO
from itertools import zip_longest

import bootstraparse.modules.parser as parser
from bootstraparse.modules import syntax

complete_list = StringIO("""
<<div
div>>
<<section
section>>
<<article
article>>
<<aside
aside>>
# H1 #
## H2 ##
### H3 ###
#### H4 ####
##### H5 #####
###### H6 ######
! S1 !
!! S2 !!
!!! S3 !!!
**
*
~~
text
""")

expected_list = [
    syntax.Linebreak, syntax.StructuralElementStartToken,
    syntax.Linebreak, syntax.StructuralElementEndToken,
    syntax.Linebreak, syntax.StructuralElementStartToken,
    syntax.Linebreak, syntax.StructuralElementEndToken,
    syntax.Linebreak, syntax.StructuralElementStartToken,
    syntax.Linebreak, syntax.StructuralElementEndToken,
    syntax.Linebreak, syntax.StructuralElementStartToken,
    syntax.Linebreak, syntax.StructuralElementEndToken,
    syntax.Linebreak, syntax.HeaderToken,
    syntax.Linebreak, syntax.HeaderToken,
    syntax.Linebreak, syntax.HeaderToken,
    syntax.Linebreak, syntax.HeaderToken,
    syntax.Linebreak, syntax.HeaderToken,
    syntax.Linebreak, syntax.HeaderToken,
    syntax.Linebreak, syntax.DisplayToken,
    syntax.Linebreak, syntax.DisplayToken,
    syntax.Linebreak, syntax.DisplayToken,
    syntax.Linebreak, syntax.EtStrongToken,
    syntax.Linebreak, syntax.EtEmToken,
    syntax.Linebreak, syntax.EtStrikethroughToken,
    syntax.Linebreak, syntax.TextToken,
    syntax.Linebreak,
]


def test_parse_line():
    list_parsed=parser.parse_line(complete_list)
    for element, expected in zip_longest(list_parsed, expected_list):
        assert element.__class__ == expected