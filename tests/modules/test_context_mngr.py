import pytest
import rich

from bootstraparse.modules import context_mngr, export, error_mngr, tools
from bootstraparse.modules import syntax as sy #sy.SemanticType, sy.TextToken, sy.Linebreak, sy.StructuralElementStartToken, sy.StructuralElementEndToken, sy.EtUlistToken, sy.EtOlistToken # noqa
from bootstraparse.modules.tools import __GLk
__XF = pytest.mark.xfail


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
    context_mngr.TableSeparatorContainer,
    context_mngr.TableRowContainer,
    context_mngr.TableCellContainer,
    context_mngr.LinebreakContainer,
]

_base_list = [sy.TextToken(["1"]), sy.TextToken(["2"]), sy.TextToken(["3"]), sy.TextToken(["4"])]
_opts = sy.OptionalToken([
    sy.OptionalVarToken([
        sy.BeAssignToken([["class", "blue"]]),
        sy.BeValueToken([123]),
    ]),
    sy.OptionalInsertToken(["var='test', number=11"]),
])
_others = {
    "header_level": "1",
    "display_level": "1",
    "col_span": "1",
    "row_span": "1",
    "url": "1",
    "test": "1",
}

_token_list_with_expected_result = [
    [
        [sy.TextToken(["1"])],
        [context_mngr.TextContainer([sy.TextToken(["1"])])],
        __GLk(1),
    ],
    [
        [
            sy.StructuralElementStartToken(["div"]),
            sy.TextToken(["1"]),
            sy.StructuralElementEndToken(["div"]),
        ],
        [
            context_mngr.SeContainer([
                sy.StructuralElementStartToken(["div"]),
                context_mngr.TextContainer([sy.TextToken(["1"])]),
                sy.StructuralElementEndToken(["div"])
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.StructuralElementStartToken(["header"]),
            sy.TextToken(["1"]),
            sy.StructuralElementEndToken(["header"]),
        ],
        [
            context_mngr.SeContainer([
                sy.StructuralElementStartToken(["header"]),
                context_mngr.TextContainer([sy.TextToken(["1"])]),
                sy.StructuralElementEndToken(["header"])
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
    ],
    [
        [
            sy.EtUlistToken([sy.TextToken(["a"])]),
            sy.Linebreak([]),
            sy.EtUlistToken([sy.TextToken(["b"])]),
            sy.Linebreak([]),
            sy.EtUlistToken([sy.TextToken(["c"])]),
            sy.EtUlistToken([sy.TextToken(["d"])]),
            sy.EtOlistToken([sy.TextToken(["aa"])]),
            sy.EtOlistToken([sy.TextToken(["bb"])]),
            sy.EtOlistToken([sy.TextToken(["cc"])]),
            sy.Linebreak([]),
            sy.EtOlistToken([sy.TextToken(["dd"])]),
            sy.Linebreak([]),
            sy.Linebreak([]),
            sy.TextToken(["1"]),
            sy.Linebreak([]),
            sy.TextToken([2]),
        ],
        [
            context_mngr.EtUlistContainer([
                sy.EtUlistToken([context_mngr.TextContainer([sy.TextToken(["a"])])]),
                sy.Linebreak([]),
                sy.EtUlistToken([context_mngr.TextContainer([sy.TextToken(["b"])])]),
                sy.Linebreak([]),
                sy.EtUlistToken([context_mngr.TextContainer([sy.TextToken(["c"])])]),
                sy.EtUlistToken([context_mngr.TextContainer([sy.TextToken(["d"])])]),
                ]),
            context_mngr.EtOlistContainer([
                sy.EtOlistToken([context_mngr.TextContainer([sy.TextToken(["aa"])])]),
                sy.EtOlistToken([context_mngr.TextContainer([sy.TextToken(["bb"])])]),
                sy.EtOlistToken([context_mngr.TextContainer([sy.TextToken(["cc"])])]),
                sy.Linebreak([]),
                sy.EtOlistToken([context_mngr.TextContainer([sy.TextToken(["dd"])])]),
                sy.Linebreak([]),
                ]),
            context_mngr.LinebreakContainer([sy.Linebreak([])]),
            context_mngr.TextContainer([sy.TextToken(["1"])]),
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
            context_mngr.TextContainer([sy.TextToken(["a"])]),
        ],
        __GLk(1),
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
            sy.HeaderToken(["#", "h1"]),
            sy.TextToken(["a"]),
            sy.HeaderToken(["##", "h2"]),
            sy.TextToken(["b"]),
            sy.HeaderToken(["###", "h3"]),
            sy.TextToken(["c"]),
            sy.HeaderToken(["####", "h4"]),
            sy.TextToken(["d"]),
            sy.HeaderToken(["#####", "h5"]),
            sy.TextToken(["e"]),
            sy.HeaderToken(["######", "h6"]),
        ],
        [
            context_mngr.HeaderContainer([
                sy.HeaderToken(["#", "h1"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["a"])]),
            context_mngr.HeaderContainer([
                sy.HeaderToken(["##", "h2"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["b"])]),
            context_mngr.HeaderContainer([
                sy.HeaderToken(["###", "h3"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["c"])]),
            context_mngr.HeaderContainer([
                sy.HeaderToken(["####", "h4"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["d"])]),
            context_mngr.HeaderContainer([
                sy.HeaderToken(["#####", "h5"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["e"])]),
            context_mngr.HeaderContainer([
                sy.HeaderToken(["######", "h6"]),
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.DisplayToken(["!", "Display"]),
            sy.TextToken(["a"]),
        ],
        [
            context_mngr.DisplayContainer([
                sy.DisplayToken(["!", "Display"]),
            ]),
            context_mngr.TextContainer([sy.TextToken(["a"])]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.TableRowToken([
                sy.TableCellToken([
                    "2",
                    sy.TextToken(["a"]),
                ]),
                sy.TableCellToken([
                    sy.TextToken(["b"]),
                ]),
            ]),
        ],
        [
            context_mngr.TableRowContainer([
                sy.TableRowToken([
                    context_mngr.TableCellContainer([
                        sy.TableCellToken([
                            sy.TableCellSizeToken(["2"]),
                            context_mngr.TextContainer([sy.TextToken(["a"])]),
                        ]),
                    ]),
                    context_mngr.TableCellContainer([
                        sy.TableCellToken([
                            context_mngr.TextContainer([sy.TextToken(["b"])]),
                        ]),
                    ]),
                ]),
            ]),
        ],
        __GLk(1),
        __XF,
    ],
    [
        [
            sy.TableRowToken([
                sy.TableCellToken([
                    sy.TableCellSizeToken(["2"]),
                    sy.TextToken(["a"]),
                ]),
                sy.TableCellToken([
                    sy.TableCellSizeToken(["3"]),
                    sy.TextToken(["b"]),
                ]),
            ]),
        ],
        [
            context_mngr.TableRowContainer([
                sy.TableRowToken([
                    context_mngr.TableCellContainer([  # MONITOR # The colspan must be taken into account
                        sy.TableCellToken([
                            sy.TableCellSizeToken(["2"]),
                            context_mngr.TextContainer([sy.TextToken(["a"])]),
                        ]),
                    ]),
                    context_mngr.TableCellContainer([
                        sy.TableCellToken([
                            sy.TableCellSizeToken(["3"]),
                            context_mngr.TextContainer([sy.TextToken(["b"])]),
                        ]),
                    ]),
                ]),
            ]),
        ],
        __GLk(1),
        __XF,
    ],
    # [
    #     [
    #         sy.TableSeparatorToken(["---", "---"]),
    #     ],
    #     [
    #         error_mngr.MismatchedContainerError,
    #     ],
    #     __GLk(1),
    # ],
    [
        [
            sy.TableRowToken([
                sy.TableCellToken([
                    sy.TextToken(["a"]),
                ]),
                sy.TableCellToken([
                    sy.TextToken(["b"]),
                ]),
            ]),
            sy.TableSeparatorToken(["---", "---"]),
            sy.TableRowToken([
                sy.TableCellToken([
                    sy.TextToken(["c"]),
                ]),
                sy.TableCellToken([
                    sy.TextToken(["d"]),
                ]),
            ]),
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
        __GLk(1),
        __XF,
    ],
    [
        [
            sy.EtOlistToken([
                sy.TextToken(["a"]),
            ]),
            _opts,
            sy.EtUlistToken([
                sy.TextToken(["b"]),
            ]),
            _opts,
        ],
        [
            context_mngr.EtOlistContainer([
                sy.EtOlistToken([context_mngr.TextContainer([sy.TextToken(["a"])])]),
            ], _opts),
            context_mngr.EtUlistContainer([
                sy.EtUlistToken([context_mngr.TextContainer([sy.TextToken(["b"])])]),
            ], _opts),
        ],
        __GLk(1),
    ],
    [  # Testing error handling
        [
            sy.StructuralElementStartToken(["div"]),
            sy.StructuralElementStartToken(["aside"]),
            sy.TextToken(["a"]),
            sy.StructuralElementEndToken(["div"]),
            sy.StructuralElementEndToken(["aside"]),
        ],
        [
            error_mngr.MismatchedContainerError,
        ],
        __GLk(1),
    ],
    [
        [
            sy.EtStrongToken(['**']),
            sy.TextToken(["a"]),
            sy.EtEmToken(['*']),
            sy.EtStrongToken(['**']),
        ],
        [
            context_mngr.EtStrongContainer([
                sy.EtStrongToken(['**']),
                context_mngr.TextContainer([sy.TextToken(["a"])]),
                context_mngr.TextContainer([sy.TextToken(["*"])]),
                sy.EtStrongToken(['**']),
            ]),
        ],
        __GLk(1),
    ],
    [
        [
            sy.Linebreak([]),
            sy.Linebreak([]),
            sy.Linebreak([]),
        ],
        [
            context_mngr.LinebreakContainer([
                sy.Linebreak([]),
                sy.Linebreak([]),
                sy.Linebreak([]),
            ]),
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
    base = context_mngr.ContextManager(lst)
    base()
    return base


@pytest.mark.parametrize("cls", _list_classes)
def test_container_init(cls):
    cls()


def test_encapsulate(base_cm):  # Robustness is tested in test_container_export_value
    base_cm.pile = _base_list[:]
    base_cm.encapsulate(1, 2)
    ctn = context_mngr.TextContainer()
    ctn.add(_base_list[1])
    ctn.add(_base_list[2])
    res = [_base_list[0], ctn, None] + _base_list[3:]
    assert base_cm.pile == res


def test_encapsulate_bad_index(base_cm):
    base_cm.pile = _base_list[:]
    with pytest.raises(IndexError):
        base_cm.encapsulate(1, 44)

    with pytest.raises(IndexError):
        base_cm.encapsulate(33, 1)

    with pytest.raises(IndexError):
        base_cm.encapsulate(2, 1)

    base_cm.encapsulate(1, 2)
    with pytest.raises(AttributeError):
        base_cm.encapsulate(2, 2)

    base_cm.pile[0] = {}
    with pytest.raises(AttributeError):
        base_cm.encapsulate(0, 0)


def test_encapsulate_bad_cm(base_cm):
    base_cm.pile[1] = sy.SemanticType([1])
    with pytest.raises(KeyError):
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

    base2 = context_mngr.BaseContainer(["test3", "test2", "test4"])
    assert base == base2
    assert base != ['test3', 'test2', 'test5']
    assert base != ['test3', 'test2']
    assert type(repr(base)) == str
    assert type(str(base)) == str
    assert ~base is None
    base.map = {'test': lambda: "test3"}
    assert base >> "test" == 'test3'
    assert base != 1
    assert hasattr(base, "get_others")
    assert hasattr(base, "get_optionals")
    assert base.get_optionals() is None
    assert base.get_others() is not None
    base2.others = _others
    assert base2 != base
    base.others = _others.copy()
    assert base == base2
    base.optionals = _opts
    assert base != base2
    base2.optionals = _opts
    assert base == base2
    base.others["test"] = "test3"
    assert base != base2
    base.debug_map()


def test_print():
    base = context_mngr.BaseContainer()
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
    print(f"Executing tests @{file_line}")
    ctx = context_mngr.ContextManager(init_list)  # noqa : F841
    # ctx.print_all()
    if isinstance(expected[0], context_mngr.BaseContainer) or isinstance(expected[0], sy.SemanticType):
        for i, e in zip(ctx(), expected):
            # rich.inspect(i)
            # rich.inspect(e)
            tools.compare(i, e)
            assert i == e
    else:
        with pytest.raises(expected[0]):
            ctx()


def test_double_call():
    ctx = context_mngr.ContextManager([sy.TextToken('test')])
    c = ctx()
    assert c == ctx()


def test_content_call_raises():
    ctx = context_mngr.ContextManager([sy.StructuralElementEndToken(["1"])])
    with pytest.raises(error_mngr.MismatchedContainerError):
        ctx()


def test_export_error():
    from bootstraparse.modules import config, pathresolver
    __config = config.ConfigLoader(pathresolver.b_path("configs/"))
    __templates = config.ConfigLoader(pathresolver.b_path("templates/"))
    em = export.ExportManager(__config, __templates)
    with pytest.raises(TypeError):
        context_mngr.TextContainer([sy.TextToken(['e']), None]).export(em)


def test_get_last_container_in_pile(base_cm):
    base_cm()
    rich.inspect(base_cm.pile[3])
    rich.inspect(base_cm.get_last_container_in_pile(3))
    assert base_cm.get_last_container_in_pile(3) == base_cm.pile[2]  # Always returns element before
    assert base_cm.get_last_container_in_pile(2) == base_cm.pile[1]
    base_cm.pile[2] = None
    assert base_cm.get_last_container_in_pile(2) == base_cm.pile[1]
    assert base_cm.get_last_container_in_pile(3) == base_cm.pile[1]
    base_cm.pile[1] = None
    assert base_cm.get_last_container_in_pile(2) == base_cm.pile[0]
    assert base_cm.get_last_container_in_pile(3) == base_cm.pile[0]
    assert base_cm.get_last_container_in_pile(4) == base_cm.pile[3]
    base_cm.pile[3] = None
    assert base_cm.get_last_container_in_pile(3) == base_cm.pile[0]
    assert base_cm.get_last_container_in_pile(4) == base_cm.pile[0]
    assert base_cm.get_last_container_in_pile(2) == base_cm.pile[0]
    tk = sy.TextToken(['e'])
    tk.line_number = 1
    base_cm.pile[1] = tk
    with pytest.raises(error_mngr.LonelyOptionalError):
        base_cm.get_last_container_in_pile(3)

    base_cm.pile[1] = None
    base_cm.pile[0] = None
    with pytest.raises(error_mngr.LonelyOptionalError):
        base_cm.get_last_container_in_pile(3)


def test_finalize_pile(base_cm):
    base_cm()
    base_cm.pile[0] = {}
    with pytest.raises(TypeError):
        base_cm.finalize_pile()
    base_cm.pile[0] = sy.TextToken(['e'])
    with pytest.raises(TypeError):
        base_cm.finalize_pile()
