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

def test_And_And():
    assert And(ff, tt)._and(tt).clauses == (ff, tt, tt)

def test_And_And_bad_arg():
    with pytest.raises(TypeError):
        And(ff, tt)._and(object()).clauses

def test_Or_Or():
    assert Or(ff, tt)._or(tt).clauses == (ff, tt, tt)

def test_Or_Or_bad_arg():
    with pytest.raises(TypeError):
        Or(ff, tt)._or(object()).clauses

def test_And_Or():
    assert And(ff, tt)._or(tt)(1)
    assert not And(ff, tt)._or(ff)(1)

def test_Or_And():
    assert Or(ff, tt)._and(tt)(1)
    assert not Or(ff, tt)._and(ff)(1)
