from bootstraparse.modules import context_mngr


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
    base.map = {'test': 'test3'}
    assert base.map == {'test': "test3"}
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
