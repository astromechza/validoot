import pytest
from mock import Mock

from validoot.exceptions import ValidationError
from validoot.decorators import validates


def test_positional_args():

    amk = Mock()
    amk.return_value = True
    bmk = Mock()
    bmk.return_value = True

    @validates(amk, bmk, None)
    def inner(a, b, c):
        return a, b, c

    assert inner(1, 2, 3) == (1, 2, 3)

    amk.assert_called_once_with(1)
    bmk.assert_called_once_with(2)


def test_position_args_fail():

    amk = Mock()
    amk.return_value = False
    amk.__str__ = Mock()
    amk.__str__.return_value = '<AlwaysFail>'

    @validates(amk)
    def inner(a):
        return a

    with pytest.raises(ValidationError) as e:
        inner(1)
    assert e.value.message == "Validation <AlwaysFail> failed for value 1 ( arg[0] )"


def test_keyword_args():

    amk = Mock()
    amk.return_value = True

    @validates(key=amk)
    def inner(key=None):
        return key

    assert inner(key='Bob') == 'Bob'

    amk.assert_called_once_with('Bob')


def test_keyword_args_fail():

    amk = Mock()
    amk.return_value = False
    amk.__str__ = Mock()
    amk.__str__.return_value = '<AlwaysFail>'

    @validates(key=amk)
    def inner(key=None):
        return key

    with pytest.raises(ValidationError) as e:
        inner(key='Bob')
    assert e.value.message == "Validation <AlwaysFail> failed for value 'Bob' ( kwarg[key] )"
