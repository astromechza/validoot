
from validoot.clauses import Clause, is_type, is_instance, between, len_between

# base clause

def test_Clause():
    assert not Clause()(1)

# is_type clause

def test_is_type():
    assert is_type(int)(1)

def test_is_type_fail():
    assert not is_type(str)(1)

def test_is_type_no_inheritance():
    assert not is_type(basestring)('')

# is_instance clause

def test_is_instance():
    assert is_instance(int)(1)

def test_is_instance_fail():
    assert not is_instance(str)(1)

def test_is_instance_inheritance():
    assert is_instance(basestring)('bob')
    assert is_instance(basestring)(u'charles')

# between clause

def test_between():
    assert between(0, 1)(0.5)
    assert not between(0, 1)(-1)
    assert not between(0, 1)(2)

# len_between clause

def test_len_between():
    assert len_between(0, 5)('bob')
    assert not len_between(0, 5)('something long')
    assert not len_between(2, 5)('')

