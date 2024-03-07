"""
This is a file for testing functions from the source code.
using pytest https://docs.pytest.org/en/8.0.x/
"""
#from __future__ import annotations

from python_package.hellop import hello_world,hello_goodbye


def hello_test():
    """
    This defines the expected usage, which can then be used in various test cases.
    Pytest will not execute this code directly, since the function does not contain the suffex "test"
    """
    hello_world()


def test_hello(unit_test_mocks: None):
    """
    This is a simple test, which can use a mock to override online functionality.
    unit_test_mocks: Fixture located in conftest.py, implictly imported via pytest.
    """
    hello_test()

def test_goodbye():
    hello_goodbye()

def test_int_hello():
    """
    This test is marked implicitly as an integration test because the name contains "_init_"
    https://docs.pytest.org/en/6.2.x/example/markers.html#automatically-adding-markers-based-on-test-names
    """
    hello_test()

def test_assert():
    """Test example"""
    assert 1 == 1

def test_string():
    """More test"""
    assert hello_world() == "string-0"
    assert hello_world(1) == "string-1"