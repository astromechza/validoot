class And(object):

    def __init__(self, *clauses):
        super(And, self).__init__()
        for clause in clauses:
            if not callable(clause):
                raise TypeError('Argument {!r} is not callable'.format(clause))
        self.clauses = clauses

    def __call__(self, value):
        for clause in self.clauses:
            if clause(value) is not True:
                return False
        return True

    def _and(self, *clauses):
        for clause in clauses:
            if not callable(clause):
                raise TypeError('Argument {!r} is not callable'.format(clause))
        self.clauses = tuple(list(self.clauses) + list(clauses))
        return self

    def _or(self, *clauses):
        return Or(*([self] + list(clauses)))

    def __str__(self):
        return "<" + ' and '.join([str(c) for c in self.clauses]) + ">"


class Or(object):

    def __init__(self, *clauses):
        super(Or, self).__init__()
        for clause in clauses:
            if not callable(clause):
                raise TypeError('Argument {!r} is not callable'.format(clause))
        self.clauses = clauses

    def __call__(self, value):
        for clause in self.clauses:
            if clause(value) is True:
                return True
        return False

    def _and(self, *clauses):
        return And(*([self] + list(clauses)))

    def _or(self, *clauses):
        for clause in clauses:
            if not callable(clause):
                raise TypeError('Argument {!r} is not callable'.format(clause))
        self.clauses = tuple(list(self.clauses) + list(clauses))
        return self

    def __str__(self):
        return "<" + ' or '.join([str(c) for c in self.clauses]) + ">"
