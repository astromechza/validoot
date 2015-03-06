from .exceptions import ValidationError

class _and_(object):

    def __init__(self, *clauses):
        for clause in clauses:
            if not callable(clause):
                raise TypeError('Argument {} is not callable'.format(clause))
        self.clauses = clauses

    def __call__(self, value):
        for clause in self.clauses:
            if clause(value) != True:
                raise ValidationError(
                    'Value {} did not pass clause {}'.format(value, clause))
        return True

class _or_(object):

    def __init__(self, *clauses):
        for clause in clauses:
            if not callable(clause):
                raise TypeError('Argument {} is not callable'.format(clause))
        self.clauses = clauses

    def __call__(self, value):
        for clause in self.clauses:
            if clause(value) == True:
                return True
        raise ValidationError('Value {} did not pass any clauses'.format(value))
