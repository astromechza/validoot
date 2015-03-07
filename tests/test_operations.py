import pytest

from validoot.operations import And, Or
from validoot.exceptions import ValidationError

def tt(v):
    return True

def ff(v):
    return False

def test_And():
    assert And(tt, tt)(1)
    assert not And(tt, ff)(1)

def test_And_bad_arg():
    with pytest.raises(TypeError):
        And(object(), tt)

def test_Or():
    assert Or(ff, tt)(1)
    assert not Or(ff, ff)(1)

def test_Or_bad_arg():
    with pytest.raises(TypeError):
        Or(object(), tt)
