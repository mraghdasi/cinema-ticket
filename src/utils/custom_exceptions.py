class UsernameValidationError(Exception):
    """
        Username Validation Error Exception
    """

    def __init__(self):
        super().__init__('Username Length Must be Between 3 and 100, You Can Only Use a-z A-Z 0-9')


class EmailValidationError(Exception):
    """
        Email Validation Error Exception
    """

    def __init__(self):
        super().__init__('Please Enter a Valid Email Address')


class PhoneNumberValidationError(Exception):
    """
        Phone Number Validation Error Exception
    """

    def __init__(self):
        super().__init__('Please Enter a Valid Phone Number')

