
class ValidationError(ValueError):
    """
    Exception indicating that a validation failed.

    Does NOT mean that the actual validation steps failed, but rather that
    a validation check failed.
    """

    def __init__(self, message):
        super(ValidationError, self).__init__(message)
