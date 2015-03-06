
from .exceptions import ValidationError

class validated(object):

    def __init__(self, *args, **kwargs):
        self.positional_validators = args
        self.keyword_validators = kwargs

    def __call__(self, func):
        self.func = func
        return self.inner

    def inner(self, *args, **kwargs):
        for i in xrange(len(self.positional_validators)):
            r = self.positional_validators[i](args[i])
            if r != True:
                raise ValidationError(
                    'Validation for position argument {:d} with value {!r} failed.'.format(i, args[i]))

        for k, v in kwargs.iteritems():
            if k in self.keyword_validators:
                r = self.keyword_validators[k](v)
                if r != True:
                    raise ValidationError(
                        'Validation for keyword argument {!s} with value {!r} failed.'.format(k, v))

        return self.func(*args, **kwargs)
