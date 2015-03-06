
# base clause

class Clause(object):

    def __init__(self):
        super(Clause, self).__init__()

    def __call__(self, value):
        return False

# type clause

class is_type(Clause):

    def __init__(self, typ):
        super(is_type, self).__init__()
        self.typ = typ

    def __call__(self, value):
        return type(value) == self.typ

class between(Clause):

    def __init__(self, lower, upper):
        super(between, self).__init__()
        self.lower = lower
        self.upper = upper

    def __call__(self, value):
        return self.lower < value < self.upper

class len_between(between):

    def __call__(self, value):
        super(len_between, self).__call__(len(value))
