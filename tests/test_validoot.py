import pytest

from validoot import ValidationError, validated, _and_, _or_, is_type, between, len_between, is_instance

@validated(_and_(is_type(int), between(0, 10)), is_type(float), key=_and_(is_instance(str), len_between(8, 20)))
def some_function(a, b, key=None):
    return a, b

def test_basic():
    assert some_function(5, 0.1, key='some string') == (5, 0.1)

def test_type_raises():
    with pytest.raises(ValidationError):
        some_function(0.5, 0.1, key='some string')

    with pytest.raises(ValidationError):
        some_function(5, 1, key='some string')

    with pytest.raises(ValidationError):
        some_function(5, 0.1, key='some')
