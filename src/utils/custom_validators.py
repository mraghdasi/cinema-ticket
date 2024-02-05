import datetime
import re

from validators import email

import src.utils.custom_exceptions as custom_exceptions
from src.utils.custom_exceptions import exception_log


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

    @staticmethod
    def username_validator(username_str):
        """
        A Function to Validate Username String
        :param username_str:
        :return:
             True Or UsernameValidationError
        """
        if re.match(r".*[a-z].*", username_str) and\
                re.match(r".*[A-Z].*", username_str) and\
                re.match(r".*[0-9].*", username_str) and\
                3 <= len(username_str) <= 100:
            return True
        else:
            raise custom_exceptions.UsernameValidationError()

    @staticmethod
    def email_validator(email_str):
        """
            A Function to Validate Email String
        :param email_str:
        :return:
            True Or EmailValidationError
        """
        if email(email_str):
            return True
        else:
            raise custom_exceptions.EmailValidationError()

    @staticmethod
    def phone_number_validator(phone_number_str):
        """
        A Function to Validate Phone Number String
        :param phone_number_str:
        :return:
        True Or PhoneNumberValidationError Or None
        """
        if len(phone_number_str) != 0:
            if re.match(r"^(09)([0-9]{9})$", phone_number_str):
                return True
            else:
                raise custom_exceptions.PhoneNumberValidationError()
        else:
            return True

    @staticmethod
    def password_validator(password_str):
        """
        A function to validate password

        :param password_str:
        :return:
        True or PasswordValidationError
        """
        length_check = re.match(r"^.{8,100}$", password_str)
        special_char_check = re.search(r"(.*[!@#$%^&*()_+\-=\[\]{};':\"\\,.<>?].*){2,}", password_str)
        uppercase_check = re.search(r"(.*[A-Z].*){2,}", password_str)
        lowercase_check = re.search(r"(.*[a-z].*){2,}", password_str)
        digit_check = re.search(r"(.*\d.*){2,}", password_str)

        if all([length_check, special_char_check, uppercase_check, lowercase_check, digit_check]):
            return True
        else:
            raise custom_exceptions.PasswordValidationError()

    @staticmethod
    def birthday_format_validator(birthday_str):
        """
        A function to validate birthday

        :param birthday_str:
        :return:
        True or BirthdayValidationError
        """

        try:
            datetime.date.fromisoformat(birthday_str)
            return True
        except ValueError:
            raise custom_exceptions.BirthdayValidationError()

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
            raise custom_exceptions.MinAgeNotPositive()

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
            raise custom_exceptions.MinAgeNotPositive()

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
