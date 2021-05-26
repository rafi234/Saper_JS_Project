import MyException


class InputError(MyException.Error):
    """Exception raised for errors in the input.

    Attributes:
        expression - input expression in which the error occurs
        message - explanation on the errors
    """

    def __init__(self, expression, message):
        self.message = message
        self.expression = expression
