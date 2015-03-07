
from validoot.clauses import (
    Clause, is_type, is_instance, between, len_between, not_negative
)


class A(object):
    pass

class B(A):
    pass

# base clause

def test_Clause():
    assert not Clause()(1)

# is_type clause

def test_is_type():
    assert is_type(int)(1)

def test_is_type_fail():
    assert not is_type(str)(1)

def test_is_type_no_inheritance():
    assert is_type(A)(A())
    assert not is_type(A)(B())

# is_instance clause

def test_is_instance():
    assert is_instance(int)(1)

def test_is_instance_fail():
    assert not is_instance(str)(1)

def test_is_instance_inheritance():
    assert is_instance(A)(A())
    assert is_instance(A)(B())
    assert not is_instance(B)(A())

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
