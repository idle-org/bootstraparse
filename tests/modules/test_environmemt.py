import bootstraparse.modules.environment as e


def test_wasInitialised():
    test_check = e.Environment()
    for k in test_check._wasInitialised.values():
        assert k is False


def test_integrity_check():
    test_check = e.Environment()
    custom_test_p = [p for p in test_check._mParams.keys()]
    custom_test_v = [False for _ in test_check._mParams.values()]
    # Test all False
    # rich.inspect(test_check)

    assert test_check.integrity_check() is False

    custom_test_v[0] = True
    test_check._wasInitialised = dict(zip(custom_test_p, custom_test_v))
    # Test first False
    # rich.inspect(test_check)

    assert test_check.integrity_check() is False

    custom_test_v[0] = False
    custom_test_v[-1] = True
    test_check._wasInitialised = dict(zip(custom_test_p, custom_test_v))
    # Test last False
    # rich.inspect(test_check)

    assert test_check.integrity_check() is False

    custom_test_v[-1] = False
    custom_test_v[len(custom_test_v)//2-1] = True
    test_check._wasInitialised = dict(zip(custom_test_p, custom_test_v))
    # Test middle False
    # rich.inspect(test_check)

    assert test_check.integrity_check() is False

    custom_test_v = [True for _ in test_check._mParams.values()]
    test_check._wasInitialised = dict(zip(custom_test_p, custom_test_v))
    # Test all True
    # rich.inspect(test_check)

    assert test_check.integrity_check() is True


def test_getter():
    test_check = e.Environment()
    for p in test_check._mParams:
        assert test_check.__getattr__(p) == test_check._mParams[p]

    test_check._sParams = {
        "test_param": "test_value"
    }
    assert test_check.test_param == "test_value"

    try:
        test_check.purposefully_non_existing_parameter
    except AttributeError:
        pass
    except Exception:
        assert False  # Not AttributeError when getting non-existing parameter

    try:
        test_check._purposefully_non_existing_parameter
    except AttributeError:
        pass
    except Exception:
        assert False  # Not AttributeError when getting underscored non-existing parameter


def test_setter():
    test_check = e.Environment()
    for p in test_check._mParams:
        test_check.__setattr__(p, "test_value")
        assert test_check._mParams[p] == "test_value"

    test_check._sParams = {
        "test_param": "test_value"
    }
    test_check.test_param = "second_test_value"
    assert test_check.test_param == "second_test_value"

    try:
        test_check.purposefully_non_existing_parameter = "test_value"
    except AttributeError:
        pass
    except Exception:
        assert False  # Not AttributeError when getting non-existing parameter

    test_check._purposefully_non_existing_parameter = "test_value"
    assert test_check._purposefully_non_existing_parameter == "test_value"


if __name__ == "__main__":
    test_setter()
