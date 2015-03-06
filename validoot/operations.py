from .exceptions import ValidationError

class _and_(object):

    def __init__(self, *clauses):
        for clause in clauses:
            if not callable(clause):
                raise TypeError('Argument {!r} is not callable'.format(clause))
        self.clauses = clauses

    def __call__(self, value):
        for clause in self.clauses:
            if clause(value) != True:
                raise ValidationError(
                    'Value {!r} did not pass clause {!r}'.format(value, clause))
        return True

class _or_(object):

    def __init__(self, *clauses):
        for clause in clauses:
            if not callable(clause):
                raise TypeError('Argument {!r} is not callable'.format(clause))
        self.clauses = clauses

    def __call__(self, value):
        for clause in self.clauses:
            if clause(value) == True:
                return True
        raise ValidationError('Value {!r} did not pass any clauses'.format(value))
