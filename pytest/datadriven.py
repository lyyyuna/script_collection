import pytest

d = {"good": "SUCCESS", "bad": "FAIL"}
d = [i for i in range(10)]

@pytest.fixture(params=d)
def parameterized_fixture(request):
    param = request.param
    return param


def test_one(parameterized_fixture):
    print parameterized_fixture


def test_two():
    pass