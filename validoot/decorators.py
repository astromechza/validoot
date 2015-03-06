
from .exceptions import ValidationError

class validates(object):

    def __init__(self, *args, **kwargs):
        self.positional_validators = args
        self.keyword_validators = kwargs

    def __call__(self, func):
        self.func = func
        return self.inner

    def inner(self, *args, **kwargs):
        for i in xrange(len(self.positional_validators)):
            if self.positional_validators[i] is not None:
                if self.positional_validators[i](args[i]) != True:
                    raise ValidationError(
                        'Validation for position argument {:d} with value {!r} failed.'.format(i, args[i]))

        for k, v in kwargs.iteritems():
            if k in self.keyword_validators:
                if self.keyword_validators[k](v) != True:
                    raise ValidationError(
                        'Validation for keyword argument {!s} with value {!r} failed.'.format(k, v))

        return self.func(*args, **kwargs)
