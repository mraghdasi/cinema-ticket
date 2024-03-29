import logging
from datetime import datetime


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


class PasswordValidationError(Exception):
    """
        Password Validation Error Exception
    """

    def __init__(self):
        super().__init__(
            'Please Enter a Valid Password (length 8-100, 2 uppercase letters, 2 digits, 2 special characters and no whitespace)')


class DateValidationError(Exception):
    """
        Date Validation Error Exception
    """

    def __init__(self):
        super().__init__('Please Enter a Valid Format of date (yyyy-mm-dd) and Make Sure You Write a Valid Date')


class MinDateValidationError(Exception):
    """
        Min Date Validation Error Exception
    """

    def __init__(self):
        super().__init__('You Are Not Old Enough To Register On This App')


class UserPasswordNotCorrect(Exception):
    """
        User Password Not Correct Exception
    """

    def __init__(self):
        super().__init__('Password Is Not Correct')


class NewPasswordsNotSame(Exception):
    """
        New Password And Confirm New Password Not Same Exception
    """

    def __init__(self):
        super().__init__('New Password and Confirm New Password are Not Same')


class MinAgeValidationError(Exception):
    """
        Min Age Not Positive Exception
    """

    def __init__(self):
        super().__init__('You Are Not Old Enough To Attend To This Movie')


class RateNotBetweenZeroAndFive(Exception):
    """
        Rate Not Between Zero And Five Exception
    """

    def __init__(self):
        super().__init__('Rate Must Be An Integer between Zero And Five')


class CardOpAmountValueError(Exception):

    def __init__(self):
        super().__init__('Please Enter Numeric Value Without Any Decimal Portions (Min 2000)!')


class LenBoundValidationError(Exception):
    def __init__(self):
        super().__init__('Please Enter Input Within The Given Length Limit!')


class LenValidationError(Exception):
    def __init__(self):
        super().__init__('The Input Length Must Be Equal To Given Length!')


class DBError(Exception):
    """
        DB Error Exception
    """

    def __init__(self):
        super().__init__('Execute or Commit Failed.')


def exception_log():
    """
    This function is a decorator that can be applied to any function to log any exceptions that occur during its execution to a file.

    Args:
        func (function): The function to be decorated

    Returns:
        function: The decorated function

    Raises:
        Exception: Any exceptions that occur during the execution of the decorated function will be logged to the file
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.basicConfig(filename='./src/logs/error-logs.txt', level=logging.ERROR)
                logging.error(
                    f" Exception in {func.__name__} : {str(e)} | DateTime : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return wrapper

    return decorator
