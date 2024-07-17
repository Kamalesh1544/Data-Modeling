class UserAccountDisableError(Exception):
    """
    Exception raised if user don't have sufficient permission

    Arguments:
        message -- any custom message
    """

    def __init__(self, message="user don't have sufficient permission"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class UserWritePermissionError(Exception):
    """
    Exception raised if user don't have sufficient permission

    Arguments:
        message -- any custom message
    """

    def __init__(self, message="user don't have sufficient permission"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
