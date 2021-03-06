"""Tests supporting data-types in py2c.tree
"""

#------------------------------------------------------------------------------
# Py2C - A Python to C++ compiler
# Copyright (C) 2014 Pradyun S. Gedam
#------------------------------------------------------------------------------


from py2c.tree import (
    NEEDED, OPTIONAL, ZERO_OR_MORE, ONE_OR_MORE,
    identifier, singleton,
    TreeError, WrongTypeError, WrongAttributeValueError,
    Node
)

from py2c.tests import Test
from nose.tools import (
    assert_raises, assert_equal, assert_is_instance, assert_not_is_instance
)

#------------------------------------------------------------------------------
# A bunch of nodes used during testing
#------------------------------------------------------------------------------
class AllIdentifierModifersNode(Node):
    """Node with all modifiers of identifier type
    """
    _fields = [
        ('f1', identifier, NEEDED),
        ('f2', identifier, OPTIONAL),
        ('f3', identifier, ZERO_OR_MORE),
        ('f4', identifier, ONE_OR_MORE),
    ]


class AllSingletonModifersNode(Node):
    """Node with all modifiers of singleton type
    """
    _fields = [
        ('f1', singleton, NEEDED),
        ('f2', singleton, OPTIONAL),
        ('f3', singleton, ZERO_OR_MORE),
        ('f4', singleton, ONE_OR_MORE),
    ]


#------------------------------------------------------------------------------
# Common test functionality
#------------------------------------------------------------------------------
class DataTypeTestBase(Test):
    """Base class for tests for custom properties of the Node specification.
    """

    def check_valid_initialization(self, arg):
        obj = self.class_(arg)
        assert_equal(obj, arg)

    def check_invalid_initialization(self, arg):
        with assert_raises(WrongAttributeValueError):
            self.class_(arg)

    def check_instance(self, value, is_):
        if is_:
            assert_is_instance(value, self.class_)
        else:
            assert_not_is_instance(value, self.class_)


#------------------------------------------------------------------------------
# Data-Type specific tests
#------------------------------------------------------------------------------
class TestIdentifier(DataTypeTestBase):
    """Tests for 'identifier' object in the definitions
    """
    class_ = identifier

    def test_valid_initialization(self):
        yield from self.yield_tests(self.check_valid_initialization, [
            ["valid_name"],
            ["a" + "_really" * 100 + "_long_name"],
            ["a"],
        ])

    def test_invalid_initialization(self):
        yield from self.yield_tests(self.check_invalid_initialization, [
            ["Invalid name"]
        ])

    def test_isinstance(self):
        yield from self.yield_tests(self.check_instance, [
            ("valid_name", True),
            ("ValidName", True),
            ("VALID_NAME", True),
            ("Valid_1_name", True),
            (identifier("valid_name"), True),
            ("_valid_name_", True),
            ("虎", True),
            ("Invalid name", False),
            ("invalid.attr", False),
            ("in_valid._attr_", False),
        ])

    def test_issubclass(self):
        class SubClass(identifier):
            pass

        assert issubclass(str, identifier)
        assert issubclass(SubClass, identifier)
        assert not issubclass(int, identifier)

    def test_equality(self):
        assert_equal(identifier("name"), "name")

    def test_repr(self):
        assert_equal(repr(identifier("a_name")), "'a_name'")
        assert_equal(repr(identifier("some_name")), "'some_name'")
        assert_equal(repr(identifier("camelCase")), "'camelCase'")

    # FIXME: Clean next later
    def test_modifiers_valid_minimal(self):
        node = AllIdentifierModifersNode()
        node.f1 = "foo"
        node.f4 = ["bar"]
        try:
            node.finalize()
        except TreeError:
            raise AssertionError(
                "Raised Exception for valid values"
            )

    def test_modifiers_valid_all(self):
        try:
            node = AllIdentifierModifersNode("foo", "bar", (), ("baz",))
            node.finalize()
        except TreeError:
            raise AssertionError(
                "Raised exception when values were proper"
            )
        else:
            assert_equal(node.f1, "foo")
            assert_equal(node.f2, "bar")
            assert_equal(node.f3, ())
            assert_equal(node.f4, ("baz",))

    # FIXME: 4 tests in one...
    def test_modifiers_invalid_values(self):
        node = AllIdentifierModifersNode()

        with assert_raises(WrongTypeError):
            node.f1 = "invalid value"

        with assert_raises(WrongTypeError):
            node.f2 = "invalid value"

        with assert_raises(WrongTypeError):
            node.f3 = ("invalid value")

        with assert_raises(WrongTypeError):
            node.f1 = ("invalid value", "invalid value 2")


class TestSingleton(DataTypeTestBase):
    """Tests for 'singleton' object in the definitions
    """
    class_ = singleton

    def test_valid_initialization(self):
        yield from self.yield_tests(self.check_valid_initialization, [
            [True],
            [False],
            [None],
        ])

    def test_invalid_initialization(self):
        yield from self.yield_tests(self.check_invalid_initialization, [
            [""],
            [0],
            [[]],
            [()],
        ])

    def test_isinstance(self):
        yield from self.yield_tests(self.check_instance, [
            (True, True),
            (False, True),
            (None, True),
            ("string", False),
            (0, False),
            (0.0, False),
            ([], False),
            ((), False),
            (object(), False),
        ])

    def test_issubclass(self):
        class SubClass(singleton):
            pass

        assert issubclass(SubClass, self.class_)
        assert issubclass(bool, self.class_)
        assert not issubclass(int, self.class_)

    def test_repr(self):
        assert_equal(repr(singleton(True)), "True")
        assert_equal(repr(singleton(False)), "False")
        assert_equal(repr(singleton(None)), "None")

    # FIXME: Generalize the next 2 and make more them comprehensive..
    def test_modifiers_valid_minimal(self):
        node = AllSingletonModifersNode()
        node.f1 = None
        node.f4 = [None, True, False]
        try:
            node.finalize()
        except TreeError:
            self.fail("Raised Exception for valid values")

    def test_modifiers_valid_all(self):
        try:
            node = AllSingletonModifersNode(True, None, (), (False,))
            node.finalize()
        except TreeError:
            self.fail("Raised exception when values were proper")
        else:
            assert_equal(node.f1, True)
            assert_equal(node.f2, None)
            assert_equal(node.f3, ())
            assert_equal(node.f4, (False,))

    # FIXME: 4 tests in one...
    def test_modifiers_invalid_values(self):
        node = AllSingletonModifersNode()

        with assert_raises(WrongTypeError):
            node.f1 = 0
        with assert_raises(WrongTypeError):
            node.f2 = 0
        with assert_raises(WrongTypeError):
            node.f3 = (0,)
        with assert_raises(WrongTypeError):
            node.f4 = (1, 2, 3)


if __name__ == '__main__':
    from py2c.tests import runmodule

    runmodule()
