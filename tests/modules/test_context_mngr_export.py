import pytest

from bootstraparse.modules import context_mngr, export
from bootstraparse.modules import syntax as sy #sy.SemanticType, sy.TextToken, sy.Linebreak, sy.StructuralElementStartToken, sy.StructuralElementEndToken, sy.EtUlistToken, sy.EtOlistToken # noqa
from bootstraparse.modules.tools import __GLk
from bootstraparse.modules import config, pathresolver

__XF = pytest.mark.xfail
_opts = sy.OptionalToken([
    sy.OptionalVarToken([
        sy.BeAssignToken([["class", "blue"]]),
        sy.BeValueToken([123]),
    ]),
    sy.OptionalInsertToken(["var='test', number=11"]),
])


class FalseHyperlink(list):
    url = "http://test.com"
    content = ["test9"]
    text = "test9"


_list_classes_expected_value = [
    [
        context_mngr.TextContainer([
            sy.TextToken(['test']),
        ]),
        "test",
        __GLk(1),
    ],
    [
        context_mngr.EtEmContainer([
            context_mngr.TextContainer([
                sy.TextToken(['test2']),
            ]),
        ]),
        "<em>test2</em>",
        __GLk(1),
    ],
    [
        context_mngr.EtStrongContainer([
            context_mngr.TextContainer([
                sy.TextToken(['test3']),
            ]),
        ]),
        "<strong>test3</strong>",
        __GLk(1),
    ],
    [
        context_mngr.EtUnderlineContainer([
            context_mngr.TextContainer([
                sy.TextToken(['test4']),
            ]),
        ]),
        "<u>test4</u>",
        __GLk(1),
    ],
    [
        context_mngr.EtStrikethroughContainer([
            context_mngr.TextContainer([
                sy.TextToken(['test5']),
            ]),
        ]),
        "<s>test5</s>",
        __GLk(1),
    ],
    [
        context_mngr.EtCustomSpanContainer([
            sy.EtCustomSpanToken(["0"]),
            context_mngr.TextContainer([
                sy.TextToken(['test6']),
            ]),
            sy.EtCustomSpanToken(["0"]),
        ]),
        "<span>test6</span>",
        __GLk(1),
    ],
    [
        context_mngr.EtUlistContainer([
            sy.EtUlistToken([
                context_mngr.TextContainer([
                    sy.TextToken(['test7']),
                ]),
            ]),
            sy.Linebreak(["\n"]),
            sy.EtUlistToken([
                context_mngr.TextContainer([
                    sy.TextToken(['test8']),
                ]),
            ]),
        ]),
        "<ul>\n<li>test7</li>\n<li>test8</li></ul>",
        __GLk(1),
    ],
    [
        context_mngr.EtOlistContainer([
            sy.EtOlistToken([
                context_mngr.TextContainer([
                    sy.TextToken(['test8']),
                ]),
            ]),
        ]),
        "<ol>\n<li>test8</li></ol>",
        __GLk(1),
    ],
    [
        context_mngr.HyperLinkContainer([
            sy.HyperlinkToken(FalseHyperlink(['test9'])),
        ]),
        "<a href=\"http://test.com\">test9</a>",
        __GLk(1),
    ],
    [
        context_mngr.SeContainer([
            sy.StructuralElementStartToken(["div"]),
            context_mngr.TextContainer([
                sy.TextToken(['test10']),
            ]),
            sy.StructuralElementEndToken(["div"]),
        ]),
        "<div>test10</div>",
        __GLk(1),
    ],
    [
        context_mngr.HeaderContainer([
            sy.HeaderToken(["#", 'test11']),
            context_mngr.TextContainer([
                sy.TextToken(['test11']),
            ]),
        ]),
        "<h1>test11</h1>",
        __GLk(1),
    ],
    [
        context_mngr.DisplayContainer([
            sy.DisplayToken(["!", "test12"]),
        ]),
        "<p class=\"display-1\">test12</p>",
        __GLk(1),
    ],
    [
        context_mngr.DisplayContainer([
            sy.DisplayToken(["!!", "test13"]),
        ]),
        "<p class=\"display-2\">test13</p>",
        __GLk(1),
    ],
    [

        context_mngr.TableRowContainer([
            context_mngr.TableCellContainer([
                context_mngr.TextContainer([sy.TextToken(["a"])]),
            ]),
            context_mngr.TableCellContainer([
                context_mngr.TextContainer([sy.TextToken(["b"])]),
            ]),
        ]),
        "<table><tr><td>a</td><td>b</td></tr></table>",
        __GLk(1),
        __XF,
    ],
    [
        [
            context_mngr.TableRowContainer([
                context_mngr.TableCellContainer([
                    context_mngr.TextContainer([sy.TextToken(["a"])]),
                ]),
                context_mngr.TableCellContainer([
                    context_mngr.TextContainer([sy.TextToken(["b"])]),
                ]),
            ]),
            context_mngr.TableSeparatorContainer([
                sy.TableSeparatorToken(["---", "---"]),
            ]),
            context_mngr.TableRowContainer([
                context_mngr.TableCellContainer([
                    context_mngr.TextContainer([sy.TextToken(["c"])]),
                ]),
                context_mngr.TableCellContainer([
                    context_mngr.TextContainer([sy.TextToken(["d"])]),
                ]),
            ]),
        ],
        "<table><tr><td>a</td><td>b</td></tr><tr></tr><tr><td>c</td><td>d</td></tr></table>",
        __GLk(1),
        __XF,
    ],
    [
        context_mngr.EtOlistContainer([
            sy.EtOlistToken([
                context_mngr.TextContainer([
                    sy.TextToken(['test13']),
                ]),
                _opts,
            ]),
        ]),
        "<ol>\n<li>test13</li></ol>",
        __GLk(1),
    ],
    [
        context_mngr.LinebreakContainer([
            sy.Linebreak([]),
        ]),
        "\n",
        __GLk(1),
    ],
    [
        context_mngr.LinebreakContainer([
            sy.Linebreak([]),
            sy.Linebreak([]),
            sy.Linebreak([]),
        ]),
        "<br />\n<br />\n",
        __GLk(1),
    ]

]

_zipped_list_classes_expected_value = [
    pytest.param(*elt[:3], marks=elt[3:], id=f"{elt[1]}") for elt in _list_classes_expected_value
]


@pytest.mark.parametrize("container, export_v, line", _zipped_list_classes_expected_value)
def test_container_export_value(container, export_v, line):
    print(line)
    __config = config.ConfigLoader(pathresolver.b_path("configs/"))
    __templates = config.ConfigLoader(pathresolver.b_path("templates/"))
    em = export.ExportManager(__config, __templates)
    assert isinstance(container, context_mngr.BaseContainer)
    assert container.export(em) == export_v
