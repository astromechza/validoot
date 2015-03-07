
from validoot.clauses import (
    Clause,
    typ, typ_or_none, inst, inst_or_none,
    between, len_between, not_negative
)


class A(object):
    pass

class B(A):
    pass

# base clause

def test_Clause():
    assert not Clause()(1)

def test_clause_and_shortcut():
    c = typ(int)._and(between(0, 10))
    assert c(1)
    assert c(9)
    assert not c(11)

def test_clause_or_shortcut():
    c = typ(int)._or(typ(float))
    assert c(1)
    assert c(1.9)
    assert not c('string')

# typ clause

def test_typ():
    assert typ(int)(1)

def test_typ_fail():
    assert not typ(str)(1)

def test_typ_no_inheritance():
    assert typ(A)(A())
    assert not typ(A)(B())

# typ_or_none clause

def test_typ_or_none():
    assert typ_or_none(int)(1)
    assert typ_or_none(int)(None)
    assert not typ_or_none(int)(2.999)

# inst clause

def test_inst():
    assert inst(int)(1)

def test_inst_fail():
    assert not inst(str)(1)

def test_inst_inheritance():
    assert inst(A)(A())
    assert inst(A)(B())
    assert not inst(B)(A())

# inst_or_none clause

def test_inst_or_none():
    assert inst_or_none(A)(A())
    assert inst_or_none(A)(B())
    assert inst_or_none(A)(None)
    assert not inst_or_none(B)(A())

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
