
from validoot.clauses import (
    Clause, typ, inst, between, len_between, not_negative
)


class A(object):
    pass

class B(A):
    pass

# base clause

def test_Clause():
    assert not Clause()(1)

# typ clause

def test_typ():
    assert typ(int)(1)

def test_typ_fail():
    assert not typ(str)(1)

def test_typ_no_inheritance():
    assert typ(A)(A())
    assert not typ(A)(B())

# inst clause

def test_inst():
    assert inst(int)(1)

def test_inst_fail():
    assert not inst(str)(1)

def test_inst_inheritance():
    assert inst(A)(A())
    assert inst(A)(B())
    assert not inst(B)(A())

# between clause

def test_between():
    assert between(0, 1)(0.5)
    assert not between(0, 1)(-1)
    assert not between(0, 1)(2)

def test_between_bounds():
    assert between(0, 1)(0)
    assert not between(0, 1)(1)
    assert not between(0, 100, lower_inc=False)(0)
    assert between(0, 100, upper_inc=True)(100)
    assert not between(0, 100, upper_inc=True)(101)

# len_between clause

def test_len_between():
    assert len_between(0, 5)('bob')
    assert not len_between(0, 5)('something long')
    assert not len_between(2, 5)('')

# not_negative clause

def test_not_negative():
    assert not_negative()(0)
    assert not_negative()(10)
    assert not not_negative()(-1)
    assert not not_negative()(-10)
