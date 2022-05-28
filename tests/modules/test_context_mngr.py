import pytest
import rich

from bootstraparse.modules import context_mngr
from bootstraparse.modules.syntax import SemanticType, TextToken

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
_base_list = [TextToken([1]), TextToken([2]), TextToken([3]), TextToken([4])]


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
    lst = [SemanticType([1]), SemanticType([2]), SemanticType([3])]
    base = context_mngr.ContextManager(lst)
    base.pile = lst

    for e, v in zip(_base_list, base_cm):
        assert e == v


def test_encapsulate(base_cm):  # TODO : be more thourough
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


def test_encapsulate_bad_cm(base_cm):
    base_cm.pile[1] = SemanticType([1])
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
    base_cm.pile = [context_mngr.BaseContainer(), context_mngr.BaseContainer(), "test", 3, context_mngr.BaseContainer()]
    base_cm.print_all()


def test_container():
    base = context_mngr.BaseContainer()
    assert base is not None
    assert base.to_container() == base
