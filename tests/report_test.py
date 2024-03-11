import pytest

from test_helpers import get_docstr, get_name, add_step


class ReportTestSuite:
    __test__ = False

    def __init__(self) -> None:
        pass


@pytest.fixture(scope="module")
def suite():
    yield suite


def test_pass(suite, json_metadata):
    """
    Success test on purpose to test report generator
    Note: this test should not make it into the reports
    """
    # Add some metadata to the test
    json_metadata["device"] = "virtual"
    json_metadata["description"] = get_docstr()
    json_metadata["active_test"] = get_name()
    json_metadata["steps"] = 0
    assert True


def test_fail(suite, json_metadata):
    """
    Fail test on purpose to test report generator
    Note: this test should not make it into the reports
    """
    # Add some metadata to the test
    json_metadata["device"] = "virtual"
    json_metadata["description"] = get_docstr()
    json_metadata["active_test"] = get_name()
    json_metadata["steps"] = 0
    assert False


def test_skip(suite, json_metadata):
    """
    Fail test on purpose to test report generator
    Note: this test should not make it into the reports
    """
    # Add some metadata to the test
    json_metadata["device"] = "virtual"
    json_metadata["description"] = get_docstr()
    json_metadata["active_test"] = get_name()
    json_metadata["steps"] = 0

    pytest.skip("Skip test")


def test_with_steps(suite, json_metadata):
    """
    Example test with multiple steps defined
    """
    # Add some metadata to the test
    json_metadata["device"] = "test device 1"
    json_metadata["active_test"] = get_name()
    json_metadata["description"] = get_docstr()
    json_metadata["steps"] = 0

    def step_1():
        assert True

    def step_2():
        assert True

    def step_3():
        assert True

    add_step(json_metadata, "example step 1", step_1)
    add_step(json_metadata, "example step 2", step_2)
    add_step(json_metadata, "example step 1", step_3)
    assert True
