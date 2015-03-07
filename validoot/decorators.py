from .exceptions import ValidationError


class validates(object):
    """
    The core decorator that attaches validators clauses for positional and
    keyword arguments.
    """

    def __init__(self, *args, **kwargs):
        self.positional_validators = args
        self.keyword_validators = kwargs

    def __call__(self, func):
        self.func = func
        return self.inner

    def inner(self, *args, **kwargs):
        for i in range(len(self.positional_validators)):
            if self.positional_validators[i] is not None:
                if self.positional_validators[i](args[i]) is not True:
                    raise ValidationError(
                        ('Validation for position argument {:d} with value '
                         '{!r} failed.').format(i, args[i]))

        for k, v in kwargs.items():
            if k in self.keyword_validators:
                if self.keyword_validators[k](v) is not True:
                    raise ValidationError(
                        ('Validation for keyword argument {!s} with value {!r}'
                         ' failed.').format(k, v))

        return self.func(*args, **kwargs)
