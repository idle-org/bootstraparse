import pytest
# import rich

from bootstraparse.modules import context_mngr, export
from bootstraparse.modules import syntax as sy #sy.SemanticType, sy.TextToken, sy.Linebreak, sy.StructuralElementStartToken, sy.StructuralElementEndToken, sy.EtUlistToken, sy.EtOlistToken # noqa
from bootstraparse.modules.tools import __GLk
__XF = pytest.mark.xfail


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
        __XF,
    ],
    [
        context_mngr.EtUnderlineContainer([
            context_mngr.TextContainer([
                sy.TextToken(['test4']),
            ]),
        ]),
        "<u>test4</u>",
        __GLk(1),
        __XF,
    ],
    [
        context_mngr.EtStrikethroughContainer([
            context_mngr.TextContainer([
                sy.TextToken(['test5']),
            ]),
        ]),
        "<s>test5</s>",
        __GLk(1),
        __XF,
    ],
    [
        context_mngr.EtCustomSpanContainer([
            context_mngr.TextContainer([
                sy.TextToken(['test6']),
            ]),
        ]),
        "<span>test6</span>",
        __GLk(1),
        __XF,
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
        context_mngr.TableMainContainer([
            context_mngr.TableHeadContainer([
                context_mngr.TableRowContainer([
                    context_mngr.TableCellContainer([
                        context_mngr.TextContainer([
                            sy.TextToken(['test13']),
                        ]),
                    ]),
                ]),
            ]),
            context_mngr.TableRowContainer([
                context_mngr.TableCellContainer([
                    context_mngr.TextContainer([
                        sy.TextToken(['test14']),
                    ]),
                ]),
            ]),
            context_mngr.TableRowContainer([
                context_mngr.TableCellContainer([
                    context_mngr.TextContainer([
                        sy.TextToken(['test15']),
                    ]),
                ]),
            ]),
        ]),
        "<table><thead><tr><td>test13</td></tr></thead><tbody><tr><td>test14</td></tr><tr><td>test15</td></tr></tbody></table>",
        __GLk(1),
        __XF,
    ],
    [
        context_mngr.LinebreakContainer([]),
        "<br/>",
        __GLk(1),
        __XF,
    ],
]

_zipped_list_classes_expected_value = [
    pytest.param(*elt[:3], marks=elt[3:], id=f"{elt[1]}") for elt in _list_classes_expected_value
]

_list_classes = [
    context_mngr.TextContainer,
    context_mngr.EtEmContainer,
    context_mngr.EtStrongContainer,
    context_mngr.EtUnderlineContainer,
    context_mngr.EtStrikethroughContainer,
    context_mngr.EtCustomSpanContainer,
    context_mngr.EtUlistContainer,
    context_mngr.EtOlistContainer,
    context_mngr.HyperLinkContainer,
    context_mngr.SeContainer,
    context_mngr.HeaderContainer,
    context_mngr.DisplayContainer,
    context_mngr.TableMainContainer,
    context_mngr.TableHeadContainer,
    context_mngr.TableRowContainer,
    context_mngr.TableCellContainer,
    context_mngr.LinebreakContainer,
]

_base_list = [sy.TextToken([1]), sy.TextToken([2]), sy.TextToken([3]), sy.TextToken([4])]

_token_list_with_expected_result = [
    [
        [sy.TextToken([1])],
        [context_mngr.TextContainer([sy.TextToken([1])])],
        __GLk(1),
    ],
    [
        [
            sy.StructuralElementStartToken(["div"]),
            sy.TextToken([1]),
            sy.StructuralElementEndToken(["div"]),
        ],
        [
            context_mngr.SeContainer([
                sy.StructuralElementStartToken(["div"]),
                context_mngr.TextContainer([sy.TextToken([1])]),
                sy.StructuralElementEndToken(["div"])
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.EtEmToken(["*"]),
            sy.TextToken(["a"]),
            sy.EtEmToken(["*"]),
        ],
        [
            context_mngr.EtEmContainer([
                sy.EtEmToken(["*"]),
                context_mngr.TextContainer([sy.TextToken(["a"])]),
                sy.EtEmToken(["*"]),
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.EtStrongToken(["**"]),
            sy.TextToken(["a"]),
            sy.EtStrongToken(["**"]),
        ],
        [
            context_mngr.EtStrongContainer([
                sy.EtStrongToken(["**"]),
                context_mngr.TextContainer([sy.TextToken(["a"])]),
                sy.EtStrongToken(["**"]),
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.EtUnderlineToken(["__"]),
            sy.TextToken(["a"]),
            sy.EtUnderlineToken(["__"]),
        ],
        [
            context_mngr.EtUnderlineContainer([
                sy.EtUnderlineToken(["__"]),
                context_mngr.TextContainer([sy.TextToken(["a"])]),
                sy.EtUnderlineToken(["__"]),
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.EtStrikethroughToken(["~~"]),
            sy.TextToken(["a"]),
            sy.EtStrikethroughToken(["~~"]),
        ],
        [
            context_mngr.EtStrikethroughContainer([
                sy.EtStrikethroughToken(["~~"]),
                context_mngr.TextContainer([sy.TextToken(["a"])]),
                sy.EtStrikethroughToken(["~~"]),
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.EtCustomSpanToken(["span", "class", "test"]),
            sy.TextToken(["a"]),
            sy.EtCustomSpanToken(["span", "class", "test"]),
        ],
        [
            context_mngr.EtCustomSpanContainer([
                sy.EtCustomSpanToken(["span", "class", "test"]),
                context_mngr.TextContainer([sy.TextToken(["a"])]),
                sy.EtCustomSpanToken(["span", "class", "test"]),
            ]),
        ],
        __GLk(1),
        __XF,
    ],
    [
        [
            sy.EtUlistToken(["a"]),
            sy.Linebreak([]),
            sy.EtUlistToken(["b"]),
            sy.Linebreak([]),
            sy.EtUlistToken(["c"]),
            sy.EtUlistToken(["d"]),
            sy.EtOlistToken(["aa"]),
            sy.EtOlistToken(["bb"]),
            sy.EtOlistToken(["cc"]),
            sy.Linebreak([]),
            sy.EtOlistToken(["dd"]),
            sy.Linebreak([]),
            sy.Linebreak([]),
            sy.TextToken([1]),
            sy.Linebreak([]),
            sy.TextToken([2]),
        ],
        [
            context_mngr.EtUlistContainer([
                sy.EtUlistToken(["a"]),
                sy.Linebreak([]),
                sy.EtUlistToken(["b"]),
                sy.Linebreak([]),
                sy.EtUlistToken(["c"]),
                sy.EtUlistToken(["d"]),
                ]),
            context_mngr.EtUlistContainer([
                sy.EtOlistToken(["aa"]),
                sy.EtOlistToken(["bb"]),
                sy.EtOlistToken(["cc"]),
                sy.Linebreak([]),
                sy.EtOlistToken(["dd"]),
                sy.Linebreak([]),
                ]),
            context_mngr.LinebreakContainer([sy.Linebreak([])]),
            context_mngr.TextContainer([sy.TextToken([1])]),
            context_mngr.LinebreakContainer([sy.Linebreak([])]),
            context_mngr.TextContainer([sy.TextToken([2])]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.HyperlinkToken(["a", "href", "http://test.com"]),
            sy.TextToken(["a"]),
        ],
        [
            context_mngr.HyperLinkContainer([
                sy.HyperlinkToken(["a", "href", "http://test.com"]),
            ]),
            sy.TextToken(["a"]),
        ],
        __GLk(1),
        __XF,
    ],
    [
        [
            sy.StructuralElementStartToken(["div"]),
            sy.TextToken(["a"]),
            sy.StructuralElementEndToken(["div"]),
        ],
        [
            context_mngr.SeContainer([
                sy.StructuralElementStartToken(["div"]),
                context_mngr.TextContainer([sy.TextToken(["a"])]),
                sy.StructuralElementEndToken(["div"])
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.StructuralElementStartToken(["div"]),
            sy.StructuralElementStartToken(["aside"]),
            sy.StructuralElementStartToken(["section"]),
            sy.StructuralElementStartToken(["article"]),
            sy.TextToken(["a"]),
            sy.StructuralElementEndToken(["article"]),
            sy.StructuralElementEndToken(["section"]),
            sy.StructuralElementEndToken(["aside"]),
            sy.StructuralElementEndToken(["div"]),
        ],
        [
            context_mngr.SeContainer([
                sy.StructuralElementStartToken(["div"]),
                context_mngr.SeContainer([
                    sy.StructuralElementStartToken(["aside"]),
                    context_mngr.SeContainer([
                        sy.StructuralElementStartToken(["section"]),
                        context_mngr.SeContainer([
                            sy.StructuralElementStartToken(["article"]),
                            context_mngr.TextContainer([sy.TextToken(["a"])]),
                            sy.StructuralElementEndToken(["article"]),
                        ]),
                        sy.StructuralElementEndToken(["section"]),
                    ]),
                    sy.StructuralElementEndToken(["aside"]),
                ]),
                sy.StructuralElementEndToken(["div"]),
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.HeaderToken(["h1"]),
            sy.TextToken(["a"]),
            sy.HeaderToken(["h2"]),
            sy.TextToken(["b"]),
            sy.HeaderToken(["h3"]),
            sy.TextToken(["c"]),
            sy.HeaderToken(["h4"]),
            sy.TextToken(["d"]),
            sy.HeaderToken(["h5"]),
            sy.TextToken(["e"]),
            sy.HeaderToken(["h6"]),
        ],
        [
            context_mngr.HeaderContainer([
                sy.HeaderToken(["h1"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["a"])]),
            context_mngr.HeaderContainer([
                sy.HeaderToken(["h2"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["b"])]),
            context_mngr.HeaderContainer([
                sy.HeaderToken(["h3"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["c"])]),
            context_mngr.HeaderContainer([
                sy.HeaderToken(["h4"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["d"])]),
            context_mngr.HeaderContainer([
                sy.HeaderToken(["h5"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["e"])]),
            context_mngr.HeaderContainer([
                sy.HeaderToken(["h6"]),
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.DisplayToken(["Display"]),
            sy.TextToken(["a"]),
        ],
        [
            context_mngr.DisplayContainer([
                sy.DisplayToken(["Display"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["a"])]),
        ],
        __GLk(1),
    ],
    # context_mngr.TableMainContainer,
    # context_mngr.TableHeadContainer,
    # context_mngr.TableRowContainer,
    # context_mngr.TableCellContainer,
    [
        [sy.TextToken([1]), sy.Linebreak([])],
        [
            context_mngr.TextContainer([sy.TextToken([1])]),
            context_mngr.LinebreakContainer([sy.Linebreak([])])
        ],
        __GLk(1),
    ],
]

_zipped_token_list_with_expected_result = [
    pytest.param(*c[:3], marks=c[3:], id=f"[{i}]: {c[1][0].__class__.__name__}")
    for i, c in enumerate(_token_list_with_expected_result)
]


@pytest.fixture
def base_cm():
    lst = _base_list[:]
    base = context_mngr.ContextManager(_base_list)
    base.pile = lst
    return base


@pytest.mark.parametrize("cls", _list_classes)
def test_container_init(cls):
    cls()


def test_context_manager(base_cm):
    lst = [sy.SemanticType([1]), sy.SemanticType([2]), sy.SemanticType([3])]
    base = context_mngr.ContextManager(lst)
    base.pile = lst

    for e, v in zip(_base_list, base_cm):
        assert e == v


def test_encapsulate(base_cm):  # Robustness is tested in test_container_export_value
    base_cm.encapsulate(1, 2)
    ctn = context_mngr.TextContainer()
    ctn.add(_base_list[1])
    ctn.add(_base_list[2])
    res = [_base_list[0], ctn, None] + _base_list[3:]
    assert base_cm.pile == res


def test_encapsulate_bad_index(base_cm):
    with pytest.raises(SystemExit):
        base_cm.encapsulate(1, 44)

    with pytest.raises(SystemExit):
        base_cm.encapsulate(33, 1)

    with pytest.raises(SystemExit):
        base_cm.encapsulate(2, 1)

    base_cm.encapsulate(1, 2)
    with pytest.raises(SystemExit):
        base_cm.encapsulate(2, 2)

    base_cm.pile[0] = {}
    with pytest.raises(AttributeError):
        base_cm.encapsulate(0, 0)


def test_encapsulate_bad_cm(base_cm):
    base_cm.pile[1] = sy.SemanticType([1])
    with pytest.raises(SystemExit):
        base_cm.encapsulate(1, 2)


def test_matched_functions(base_cm):
    base_cm._add_matched("test", 2)
    assert base_cm.matched_elements == {'test': [2]}
    base_cm._add_matched("test", 3)
    assert base_cm.matched_elements == {'test': [2, 3]}
    base_cm._add_matched("test2", 4)
    assert base_cm.matched_elements == {'test': [2, 3], 'test2': [4]}
    assert base_cm._get_matched("test") == 3
    assert base_cm._get_matched("test2") == 4
    assert base_cm._get_matched("test") == 2
    with pytest.raises(IndexError):
        base_cm._get_matched("test2")
    with pytest.raises(KeyError):
        assert base_cm._get_matched("test3")


def test_context_mngr():
    base = context_mngr.BaseContainer()
    assert base is not None
    assert base.class_name() == 'BaseContainer'
    base.add('test')
    assert base[0] == 'test'
    assert len(base) == 1
    base.add('test2')
    assert base[1] == 'test2'
    assert base.validate([]) is True
    assert base.validate(['test']) is False
    assert base.debug_map() is None
    assert [x for x in base] == ['test', 'test2']
    base[0] = "test3"
    assert base[0] == 'test3'
    base.add("test4")
    assert base[0:2] == ['test3', 'test2']
    assert base.__getslice__(0, 2) == ['test3', 'test2']
    assert base == ['test3', 'test2', 'test4']
    assert base != ['test3', 'test2', 'test5']
    assert base != ['test3', 'test2']
    assert type(repr(base)) == str
    assert type(str(base)) == str
    assert ~base == []
    base.map = {'test': lambda: "test3"}
    assert base >> "test" == 'test3'
    assert base != 1


def test_base_container_with_optionals():
    base = context_mngr.BaseContainerWithOptionals()
    assert base is not None

    assert base.class_name() == 'BaseContainerWithOptionals'
    assert base.debug_map() is None

    base.add('test')
    assert base[0] == 'test'
    assert len(base) == 1

    assert base.fetch_html_insert() == []

    class OI:
        label = 'optional:insert'

    class CI:
        label = 'optional:class'

    i, c = OI(), CI()
    base.optionals = [i, c]
    assert base.fetch_html_insert() == [i]
    assert base.fetch_class_insert() == [c]


def test_print():
    base = context_mngr.BaseContainerWithOptionals()
    assert base is not None
    base.print_all()
    base.content = [context_mngr.BaseContainer(), context_mngr.BaseContainer(), "test", 3, context_mngr.BaseContainer()]
    base.print_all()


def test_print_cm(base_cm):
    base_cm.print_all()
    bc = context_mngr.BaseContainer()
    bc.add('test')
    base_cm.pile = [bc, bc, "test", 3, bc]
    base_cm.print_all()


def test_container():
    base = context_mngr.BaseContainer()
    assert base is not None
    assert base.to_container() == base


@pytest.mark.parametrize("init_list, expected, file_line", _zipped_token_list_with_expected_result)
def test_context_call(init_list, expected, file_line):
    ctx = context_mngr.ContextManager(init_list)  # noqa : F841
    assert ctx() == expected


def test_content_call_raises():
    ctx = context_mngr.ContextManager([sy.StructuralElementEndToken(["1"])])
    with pytest.raises(SystemExit):
        ctx()


@pytest.mark.parametrize("container", _list_classes)
def test_container_export(container, base_cm):
    em = export.ExportManager(None, None)
    assert type(container().export(em)) == str


@pytest.mark.parametrize("container, export_v, line", _zipped_list_classes_expected_value)
def test_container_export_value(container, export_v, line):
    em = export.ExportManager(None, None)
    assert isinstance(container, context_mngr.BaseContainer)
    assert container.export(em) == export_v


def test_export_error():
    em = export.ExportManager(None, None)
    with pytest.raises(SystemExit):
        context_mngr.TextContainer([sy.TextToken(['e']), None]).export(em)
