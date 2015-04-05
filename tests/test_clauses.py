import pytest

from validoot.clauses import (
    Clause,
    typ, typ_or_none, inst, inst_or_none,
    at_least, at_most,
    between, len_between,
    regex,
    list_of,
    dict_of,
    list_of_typ,
    list_of_inst,
    dict_of_typ,
    dict_of_inst
)


# HACKS for python2 vs python3 module names
try:
    import __builtin__
    BI = '__builtin__'
except:
    BI = 'builtins'
# end HACKS


def meta_test(validator, good=list(), bad=list()):
    for g in good:
        assert validator(g)
    for b in bad:
        assert not validator(b)


class A(object):
    pass


class B(A):
    pass


def test_Clause():
    meta_test(Clause(), bad=[1])

    assert str(Clause()) == '<always fails>'
    assert repr(Clause()) == '<always fails>'


def test_clause_and_shortcut():
    meta_test(
        typ(int)._and(between(0, 10)),
        good=[1, 9],
        bad=[11]
    )

    assert str(typ(int)._and(between(0, 10))) == '<<type {BI}.int> and <in range [0..10)>>'.format(BI=BI)


def test_clause_or_shortcut():
    meta_test(
        typ(int)._or(typ(float)),
        good=[1, 1.9],
        bad=['string']
    )

    assert str(typ(int)._or(typ(float))) == '<<type {BI}.int> or <type {BI}.float>>'.format(BI=BI)


# typ clause
def test_typ():
    meta_test(
        typ(int),
        good=[1, -1],
        bad=['string']
    )
    assert str(typ(int)) == '<type {BI}.int>'.format(BI=BI)


def test_typ_no_inheritance():
    meta_test(
        typ(A),
        good=[A()],
        bad=[B()]
    )

    assert str(typ(A)) == '<type test_clauses.A>'


# typ_or_none clause
def test_typ_or_none():
    meta_test(
        typ_or_none(int),
        good=[1, None],
        bad=[2.999]
    )

    assert str(typ_or_none(int)) == '<type {BI}.int or None>'.format(BI=BI)


# inst clause
def test_inst_inheritance():
    meta_test(
        inst(A),
        good=[A(), B()],
        bad=[object()]
    )

    assert str(inst(int)) == '<instance of {BI}.int>'.format(BI=BI)


# inst_or_none clause
def test_inst_or_none():
    meta_test(
        inst_or_none(A),
        good=[A(), B(), None],
        bad=[object()]
    )

    assert str(inst_or_none(B)) == '<instance of test_clauses.B or None>'


# at_least clause
def test_at_least():
    meta_test(
        at_least(15.5),
        good=[20, 15.5],
        bad=[10]
    )
    meta_test(
        at_least(15.5, inclusive=False),
        good=[20],
        bad=[10, 15.5]
    )

    assert str(at_least(0.5)) == '<at least 0.5 (inclusive)>'
    assert str(at_least(0.5, inclusive=False)) == '<at least 0.5 (exclusive)>'


# at_most clause
def test_at_most():
    meta_test(
        at_most(15.5),
        good=[10, 15.5],
        bad=[20]
    )
    meta_test(
        at_most(15.5, inclusive=False),
        good=[10],
        bad=[20, 15.5]
    )

    assert str(at_most(0.5)) == '<at most 0.5 (inclusive)>'
    assert str(at_most(0.5, inclusive=False)) == '<at most 0.5 (exclusive)>'


# between clause
def test_between():
    meta_test(
        between(0, 1),
        good=[0.5],
        bad=[-1, 2, 1]
    )

    assert str(between(0, 1)) == '<in range [0..1)>'


def test_between_bounds():
    assert between(0, 1)(0)
    assert not between(0, 1)(1)
    assert not between(0, 100, lower_inc=False)(0)
    assert between(0, 100, upper_inc=True)(100)
    assert not between(0, 100, upper_inc=True)(101)

    assert str(between(0, 100, lower_inc=False)) == '<in range (0..100)>'
    assert str(between(0, 100, upper_inc=True)) == '<in range [0..100]>'


# len_between clause
def test_len_between():
    assert len_between(0, 5)('bob')
    assert not len_between(0, 5)('something long')
    assert not len_between(2, 5)('')

    assert str(len_between(0, 5)) == '<length in range [0..5)>'


# regex clause
def test_regex():
    assert regex(r'\d{4}')('0000')
    assert not regex(r'\d{4}')('aaaa')
    assert not regex(r'\d{4}')('0000a')

    assert str(regex(r'\d{4}')) == "<regex match '^\d{4}$'>"

# list_of
def test_list_of():
    meta_test(
        list_of(typ(int)),
        good=[[1, 2, 3, 4], []],
        bad=[{1: 2}, [1, 2, 3, 'lol']]
    )

    with pytest.raises(TypeError):
        list_of(object())

    assert str(list_of(typ(float))) == '<list of <type {BI}.float>>'.format(BI=BI)

# dict_of
def test_dict_of():
    meta_test(
        dict_of(typ(str), typ(int)),
        good=[{'a': 1, 'b': 2, 'd': 3}, {}],
        bad=[{'a': 1, 'b': 2, 'd': 'straaang'}, None],
    )

    with pytest.raises(TypeError):
        dict_of(object(), typ(int))

    with pytest.raises(TypeError):
        dict_of(typ(int), object())

    assert str(dict_of(typ(str), typ(float))) == '<dict of <type {BI}.str> -> <type {BI}.float>>'.format(BI=BI)


# list_of_typ
def test_list_of_typ():
    meta_test(
        list_of_typ(int),
        good=[[1, 2, 3, 4], []],
        bad=[{1: 2}, [1, 2, 3, 'lol']]
    )


# dict_of_typ
def test_dict_of_typ():
    meta_test(
        dict_of_typ(str, int),
        good=[{'a': 1, 'b': 2, 'd': 3}, {}],
        bad=[{'a': 1, 'b': 2, 'd': 'straaang'}, None],
    )


# list_of_inst
def test_list_of_inst():
    meta_test(
        list_of_inst(A),
        good=[[A(), A()], [A(), B()], []],
        bad=[[object()], [1, 2, 3, 'lol']]
    )


# dict_of_inst
def test_dict_of_inst():
    meta_test(
        dict_of_inst(A, B),
        good=[{A(): B(), B(): B()}, {}],
        bad=[{A(): A(), B(): A()}, None],
    )