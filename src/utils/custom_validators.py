import re

from validators import email

import src.utils.custom_exceptions as custom_exceptions
from src.utils.custom_exceptions import exception_log
from src.utils.utils import hash_string


class Validator:
    @staticmethod
    def validate(string: str, validator_functions: tuple):
        """
        Check Multi (Or One) Validation Functions on String, If All Of That Are Returning True,
        This Function Will Return True,  But If Some Of Them Returning Exception Message,
         It Will Return a Multi Line String Of Exception Messages.
        :param string:
        :param validator_functions:
        :return:
        True Or String of Exceptions Messages
        """
        list_of_results = [validate(string)
                           for validate in validator_functions]
        list_of_messages = list(
            filter(lambda x: True if not x else False, list_of_results))
        if len(list_of_messages) > 0:
            return ' \n'.join(list_of_messages)
        else:
            return True

    @staticmethod
    def username_validator(username_str):
        """
        A Function to Validate Username String
        :param username_str:
        :return:
             username_str Or UsernameValidationError
        """
        if re.match(r"^[a-zA-Z0-9]{3,100}$", username_str):
            return True
        else:
            return str(custom_exceptions.UsernameValidationError())

    @staticmethod
    def email_validator(email_str):
        """
            A Function to Validate Email String
        :param email_str:
        :return:
            email_str Or EmailValidationError
        """
        if email(email_str):
            return True
        else:
            return str(custom_exceptions.EmailValidationError())

    @staticmethod
    def phone_number_validator(phone_number_str):
        """
        A Function to Validate Phone Number String
        :param phone_number_str:
        :return:
        phone_number_str Or PhoneNumberValidationError Or None
        """
        if len(phone_number_str) != 0:
            if re.match(r"^(09)([0-9]{9})$", phone_number_str):
                return True
            else:
                return str(custom_exceptions.PhoneNumberValidationError())
        else:
            return True

    @staticmethod
    def password_validator(password_str):
        """
        A function to validate password

        :param password_str:
        :return:
        hashed password or PasswordValidationError
        """
# Test
        if re.match(r'^((?=(?:.*[A-Z]){2,})(?=(?:.*\d){2,})(?=(?:.*[\W_]){2,})[A-Za-z\d\W_]{8})+$', password_str):
            return True
        else:
            return str(custom_exceptions.PasswordValidationError())

    @staticmethod
    def birthday_format_validator(birthday_str):
        """
        A function to validate birthday

        :param birthday_str:
        :return:
        birthday or BirthdayValidationError
        """
#  import datetime
# >>> def validate(date_text):
#         try:
#             datetime.date.fromisoformat(date_text)
#         except ValueError:
#             raise ValueError("Incorrect data format, should be YYYY-MM-DD")

        if re.match(r'^[0-9]{4}/[0-9]{2}/[0-9]{2}$', birthday_str):
            year, month, day = map(int, birthday_str.split('/'))
            if not 1300 <= year <= 1390:
                return str(custom_exceptions.BirthdayValidationError())
            elif not 1 <= month <= 12:
                return str(custom_exceptions.BirthdayValidationError())
            elif (1 <= month <= 6) and (not (1 <= day <= 31)):
                return str(custom_exceptions.BirthdayValidationError())
            elif 7 <= month <= 11 and not 1 <= day <= 30:
                return str(custom_exceptions.BirthdayValidationError())
            elif month == 12 and not 1 <= day <= 29:
                return str(custom_exceptions.BirthdayValidationError())
            return True
        else:
            return str(custom_exceptions.BirthdayValidationError())

    @staticmethod
    def min_age_validator(min_age):
        """
        A function to validate min age bigger than 0

        :param min_age:
        :return:
            True Or Message of MinAgeNotPositive Exception
        """

        if min_age >= 0:
            return True
        else:
            return str(custom_exceptions.MinAgeNotPositive())

    @staticmethod
    def rate_validator(rate):
        """
        A function to validate rate is between 0 and 5

        :param rate:
        :return:
            True Or Message of RateNotBetweenZeroAndFive Exception
        """

        if 0 <= rate <= 5:
            return True
        else:
            return str(custom_exceptions.MinAgeNotPositive())

    @staticmethod
    @exception_log()
    def len_validator(str_input: str, length: int):
        """
       A function to validate the length of a string.

       Parameters
       ----------
       str_input : str
           The string to be validated.
       length : int
           The length of the string.

       Returns
       -------
       bool
           Returns True if the length of the string is equal to the length,
           otherwise raises an exception.

       Raises
       ------
       Exception
           If the length is not met, an exception is raised with a message
           indicating the expected maximum length.
       """
        if len(str_input) == length:
            return True
        else:
            raise Exception(f'Length Must Be {length}')

    @staticmethod
    @exception_log()
    def value_validator(value: int, max_value: int):
        if value >= max_value:
            return True
        else:
            raise Exception(f'Value Must Be Greater Than {max}')
