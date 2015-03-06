import pytest

from validoot import ValidationError, validated, _and_, _or_, is_type, between, len_between

@validated(_and_(is_type(int), between(0, 10)), is_type(float), key=_and_(is_type(str), len_between(8, 20)))
def some_function(a, b, key=None):
    return a, b

def test_basic():
    assert some_function(5, 0.1, 'some string')

def test_type_raises():
    with pytest.raises(ValidationError):
        assert some_function(0.5, 0.1, 'some string')

    with pytest.raises(ValidationError):
        assert some_function(5, 1, 'some string')

    with pytest.raises(ValidationError):
        assert some_function(5, 1, 'some')

