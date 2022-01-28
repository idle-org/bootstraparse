import bootstraparse.modules.environment as e
import rich


def test_wasInitialised():
    testenv = e.environment()
    for k in testenv._wasInitialised.values():
        assert k is False


def test_integritycheck():
    testcheck = e.environment()
    customtest_p = [p for p in testcheck._mParams.keys()]
    customtest_v = [False for p in testcheck._mParams.values()]
    # Test all False

    # rich.inspect(testcheck)
    assert testcheck.integritycheck() is False

    customtest_v[0] = True
    testcheck._wasInitialised = dict(zip(customtest_p, customtest_v))
    # Test first False

    # rich.inspect(testcheck)
    assert testcheck.integritycheck() is False

    customtest_v[0] = False
    customtest_v[-1] = True
    testcheck._wasInitialised = dict(zip(customtest_p, customtest_v))
    # Test last False

    # rich.inspect(testcheck)
    assert testcheck.integritycheck() is False

    customtest_v[-1] = False
    customtest_v[len(customtest_v)//2-1] = True
    testcheck._wasInitialised = dict(zip(customtest_p, customtest_v))
    # Test middle False

    # rich.inspect(testcheck)
    assert testcheck.integritycheck() is False

    customtest_v = [True for p in testcheck._mParams.values()]
    testcheck._wasInitialised = dict(zip(customtest_p, customtest_v))
    # Test all True

    # rich.inspect(testcheck)
    assert testcheck.integritycheck() is True


if __name__ == "__main__":
    test_integritycheck()
