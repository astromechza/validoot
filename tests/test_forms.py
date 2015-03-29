import pytest
from validoot import ValidationError, typ, validates

@validates(typ(int))
def BBB(o):
    """docdoc"""
    return o


def test_method_decorator():

    @validates(typ(int))
    def b(o):
        """docdoc"""
        return o

    assert BBB(1) == 1
    assert b(1) == 1

    with pytest.raises(ValidationError):
        BBB('string')

    with pytest.raises(ValidationError):
        b('string')

    assert BBB.__name__ == 'BBB'
    assert BBB.__module__ == 'test_forms'
    assert BBB.__doc__ == 'docdoc'

    assert b.__name__ == 'b'
    assert b.__module__ == 'test_forms'
    assert b.__doc__ == 'docdoc'


def test_class_method_decorator():

    class A(object):

        @validates(typ(int))
        @classmethod
        def b(cls, o):
            """docdoc"""
            return o

    assert A.b(1) == 1

    with pytest.raises(ValidationError):
        A.b('string')


    assert A.b.__name__ == 'b'
    assert A.b.__module__ == 'test_forms'
    assert A.b.__doc__ == 'docdoc'


def test_static_method_decorator():

    class A(object):

        @staticmethod
        @validates(typ(int))
        def b(o):
            """docdoc"""
            return o

    assert A.b(1) == 1

    with pytest.raises(ValidationError):
        A.b('string')

    assert A.b.__name__ == 'b'
    assert A.b.__module__ == 'test_forms'
    assert A.b.__doc__ == 'docdoc'


def test_instance_method_decorator():

    class A(object):

        @validates(typ(int))
        def b(self, o):
            """docdoc"""
            return o

    assert A().b(1) == 1

    with pytest.raises(ValidationError):
        A().b('string')

    assert A().b.__name__ == 'b'
    assert A().b.__module__ == 'test_forms'
    assert A().b.__doc__ == 'docdoc'


def test_constructor_decorator():

    @validates(typ(int))
    class A(object):
        """docdoc"""

        def __init__(self, o):
            self.o = o

    assert A(1).o == 1

    with pytest.raises(ValidationError):
        A('string')

    assert A.__name__ == 'A'
    assert A.__module__ == 'test_forms'
    assert A.__doc__ == 'docdoc'
