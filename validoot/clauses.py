class Clause(object):

    def __init__(self):
        super(Clause, self).__init__()

    def __call__(self, value):
        return False


class typ(Clause):

    def __init__(self, t):
        super(typ, self).__init__()
        self._type = t

    def __call__(self, value):
        return type(value) == self._type


class inst(typ):

    def __call__(self, value):
        return isinstance(value, self._type)


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


class not_negative(Clause):
    def __call__(self, value):
        return value >= 0
