class Clause(object):

    def __init__(self):
        super(Clause, self).__init__()

    def __call__(self, value):
        return False

class is_type(Clause):

    def __init__(self, typ):
        super(is_type, self).__init__()
        self.typ = typ

    def __call__(self, value):
        return type(value) == self.typ

class is_instance(Clause):
    def __init__(self, inst):
        super(is_instance, self).__init__()
        self.inst = inst

    def __call__(self, value):
        return isinstance(value, self.inst)

class between(Clause):

    def __init__(self, lower, upper, lower_inclusive=True, upper_inclusive=False):
        super(between, self).__init__()
        self.lower = lower
        self.upper = upper
        self.lower_inclusive = lower_inclusive
        self.upper_inclusive = upper_inclusive

    def __call__(self, value):
        if self.lower_inclusive:
            if value < self.lower:
                return False
        elif value <= self.lower:
            return False

        if self.upper_inclusive:
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

