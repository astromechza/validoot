import re

from .operations import And, Or


class Clause(object):

    def __init__(self):
        super(Clause, self).__init__()

    def __call__(self, value):
        return False

    def _and(self, *clauses):
        return And(*([self] + list(clauses)))

    def _or(self, *clauses):
        return Or(*([self] + list(clauses)))


class typ(Clause):

    def __init__(self, t):
        super(typ, self).__init__()
        self._type = t

    def __call__(self, value):
        return type(value) == self._type


class typ_or_none(typ):

    def __call__(self, value):
        return value is None or super(typ_or_none, self).__call__(value)


class inst(typ):

    def __call__(self, value):
        return isinstance(value, self._type)


class inst_or_none(inst):

    def __call__(self, value):
        return value is None or super(inst_or_none, self).__call__(value)


class at_least(Clause):
    def __init__(self, value, inclusive=True):
        super(at_least, self).__init__()
        self.value = value
        self.inclusive = inclusive

    def __call__(self, value):
        if self.inclusive:
            return value >= self.value
        else:
            return value > self.value


class at_most(Clause):
    def __init__(self, value, inclusive=True):
        super(at_most, self).__init__()
        self.value = value
        self.inclusive = inclusive

    def __call__(self, value):
        if self.inclusive:
            return value <= self.value
        else:
            return value < self.value


class between(Clause):

    def __init__(self, lower, upper, lower_inc=True, upper_inc=False):
        super(between, self).__init__()
        self.lower = lower
        self.upper = upper
        self.lower_inc = lower_inc
        self.upper_inc = upper_inc

    def __call__(self, value):
        if self.lower_inc:
            if value < self.lower:
                return False
        elif value <= self.lower:
            return False

        if self.upper_inc:
            if value > self.upper:
                return False
        elif value >= self.upper:
            return False

        return True


class len_between(between):

    def __call__(self, value):
        return super(len_between, self).__call__(len(value))


class regex(Clause):

    def __init__(self, r, entire_string=True, flags=0):
        super(regex, self).__init__()

        if entire_string:
            if not r.startswith('^'):
                r = '^' + r
            if not r.endswith('$') and not r.endswith('\\$'):
                r = r + '$'

        self.reg = re.compile(r, flags=flags)

    def __call__(self, value):
        return self.reg.match(value) is not None


class list_of(Clause):

    def __init__(self, clause):
        super(list_of, self).__init__()

        if not callable(clause):
            raise TypeError('Clause must be callable')

        self._clause = clause

    def __call__(self, value):
        if type(value) == list:
            for l in value:
                if not self._clause(l):
                    return False
            return True
        return False


class dict_of(Clause):

    def __init__(self, clause1, clause2):
        super(dict_of, self).__init__()

        if not callable(clause1):
            raise TypeError('Clause 1 must be callable')

        if not callable(clause2):
            raise TypeError('Clause 2 must be callable')

        self._clause1 = clause1
        self._clause2 = clause2

    def __call__(self, value):
        if type(value) == dict:
            for k, v in value.items():
                if not self._clause1(k) or not self._clause2(v):
                    return False
            return True
        return False


class list_of_typ(list_of):
    def __init__(self, t):
        super(list_of_typ, self).__init__(typ(t))


class list_of_inst(list_of):
    def __init__(self, t):
        super(list_of_inst, self).__init__(inst(t))


class dict_of_typ(dict_of):
    def __init__(self, t1, t2):
        super(dict_of_typ, self).__init__(typ(t1), typ(t2))


class dict_of_inst(dict_of):
    def __init__(self, t1, t2):
        super(dict_of_inst, self).__init__(inst(t1), inst(t2))