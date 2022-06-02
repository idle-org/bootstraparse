import pytest

from bootstraparse.modules import context_mngr, export
from bootstraparse.modules import syntax as sy #sy.SemanticType, sy.TextToken, sy.Linebreak, sy.StructuralElementStartToken, sy.StructuralElementEndToken, sy.EtUlistToken, sy.EtOlistToken # noqa
from bootstraparse.modules.tools import __GLk
__XF = pytest.mark.xfail
_opts = sy.OptionalToken([
    sy.OptionalVarToken([
        sy.BeAssignToken([["class", "blue"]]),
        sy.BeValueToken([123]),
    ]),
    sy.OptionalInsertToken(["var='test', number=11"]),
])

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
        ]),
        "<ul><li>test7</li></ul>",
        __GLk(1),
        __XF,
    ],
    [
        context_mngr.EtOlistContainer([
            sy.EtOlistToken([
                context_mngr.TextContainer([
                    sy.TextToken(['test8']),
                ]),
            ]),
        ]),
        "<ol><li>test8</li></ol>",
        __GLk(1),
        __XF,
    ],
    [
        context_mngr.HyperLinkContainer([
            context_mngr.TextContainer([
                sy.TextToken(['test9']),
            ]),
        ]),
        "<a href=\"test9\">test9</a>",
        __GLk(1),
        __XF,
    ],
    [
        context_mngr.SeContainer([
            context_mngr.TextContainer([
                sy.TextToken(['test10']),
            ]),
        ]),
        "<div>test10</div>",
        __GLk(1),
        __XF,
    ],
    [
        context_mngr.HeaderContainer([
            context_mngr.TextContainer([
                sy.HeaderToken(["#", 'test11']),
                sy.TextToken(['test11']),
            ]),
        ]),
        "<h1>test11</h1>",
        __GLk(1),
        __XF,
    ],
    [
        context_mngr.DisplayContainer([
            context_mngr.TextContainer([
                sy.TextToken(['test12']),
            ]),
        ]),
        "<display>test12</display>",
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
        ],
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
        [
            context_mngr.EtOlistContainer([
                sy.EtOlistToken([
                    context_mngr.TextContainer([
                        sy.TextToken(['test13']),
                    ]),
                    _opts,
                ]),
            ]),
        ],
        "<ol><li>test13</li></ol>",
        __GLk(1),
        __XF,
    ],

]

_zipped_list_classes_expected_value = [
    pytest.param(*elt[:3], marks=elt[3:], id=f"{elt[1]}") for elt in _list_classes_expected_value
]


@pytest.mark.parametrize("container, export_v, line", _zipped_list_classes_expected_value)
def test_container_export_value(container, export_v, line):
    print(line)
    em = export.ExportManager(None, None)
    assert isinstance(container, context_mngr.BaseContainer)
    assert container.export(em) == export_v
