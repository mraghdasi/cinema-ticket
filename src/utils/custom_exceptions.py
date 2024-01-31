import logging


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
                logging.basicConfig(filename='../logs/error-logs.txt', level=logging.ERROR)
                logging.error(f" Exception in {func.__name__} : {str(e)}")

        return wrapper

    return decorator
