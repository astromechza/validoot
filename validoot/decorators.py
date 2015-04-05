from .exceptions import ValidationError

import wrapt


class validates(object):
    """
    The core decorator that attaches validators clauses for positional and
    keyword arguments.

    The wrapt.decorator add-in does most of the heavy lifting such as handling
    class/static/instance methods and renaming function attributes.
    """

    def __init__(self, *args, **kwargs):
        self.positional_validators = args
        self.keyword_validators = kwargs

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        for i in range(len(self.positional_validators)):
            if self.positional_validators[i] is not None:
                if self.positional_validators[i](args[i]) is not True:
                    raise ValidationError("Validation {!s} failed for value {!r} ( arg[{:d}] )".format(
                        self.positional_validators[i], args[i], i))

        for k, v in kwargs.items():
            if k in self.keyword_validators:
                if self.keyword_validators[k](v) is not True:
                    raise ValidationError("Validation {!s} failed for value {!r} ( kwarg[{!s}] )".format(
                        self.keyword_validators[k], v, k))

        return wrapped(*args, **kwargs)
