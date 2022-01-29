from logging import exception
import bootstraparse.modules.environment as e


def test_wasInitialised():
    testcheck = e.environment()
    for k in testcheck._wasInitialised.values():
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


def test_getter():
    testcheck = e.environment()
    for p in testcheck._mParams:
        assert testcheck.__getattr__(p) == testcheck._mParams[p]

    testcheck._sParams = {
        "testparam": "testvalue"
    }
    assert testcheck.testparam == "testvalue"

    try:
        testcheck.purposefullyunexistingparameter
    except AttributeError:
        pass
    except Exception:
        assert False  # Not AttributeError when getting unexisting parameter

    try:
        testcheck._purposefullyunexistingparameter
    except AttributeError:
        pass
    except Exception:
        assert False  # Not AttributeError when getting _unexisting parameter


def test_setter():
    testcheck = e.environment()
    for p in testcheck._mParams:
        testcheck.__setattr__(p, "testvalue")
        assert testcheck._mParams[p] == "testvalue"

    testcheck._sParams = {
        "testparam": "testvalue"
    }
    testcheck.testparam = "secondtestvalue"
    assert testcheck.testparam == "secondtestvalue"

    try:
        testcheck.purposefullyunexistingparameter = "testvalue"
    except AttributeError:
        pass
    except Exception:
        assert False  # Not AttributeError when getting unexisting parameter

    testcheck._purposefullyunexistingparameter = "testvalue"
    assert testcheck._purposefullyunexistingparameter == "testvalue"


if __name__ == "__main__":
    test_setter()
