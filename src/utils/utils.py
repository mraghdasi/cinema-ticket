import hashlib
import hmac
import re

from validators import email

from main import secret_key
import src.utils.custom_exceptions as custom_exceptions


def hash_string(string):
    """
    Return A Hashed String From An Input String
    :param string:
    :return:
        Hashed String
    """
    return hmac.new(secret_key.encode('utf-8'), string.encode('utf-8'), hashlib.sha256).hexdigest()


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
            return username_str
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
            return email_str
        else:
            raise custom_exceptions.EmailValidationError()

    @staticmethod
    def phone_number_validator(phone_number_str):
        """
        A Function to Validate Phone Number String
        :param phone_number_str:
        :return:
        phone_number_str Or PhoneNumberValidationError Or None
        """
        if phone_number_str:
            if re.match(r"^(09)([0-9]{9})$", phone_number_str):
                return phone_number_str
            else:
                raise custom_exceptions.PhoneNumberValidationError()
        else:
            return None

    @staticmethod
    def password_validator(password_str):
        '''
        A function to validate password

        :param password_str:
        :return:
        hashed password or PasswordValidationError
        '''

        if re.match(r'^(?=(?:.*[A-Z]){2,})(?=(?:.*\d){2,})(?=(?:.*[\W_]){2,})[A-Za-z\d\W_]{8,100}$', password_str):
            return hash_string(password_str)
        else:
            return custom_exceptions.PasswordValidationError()

    @staticmethod
    def birthday_format_validator(birthday_str):
        '''
        A function to validate birthday

        :param birthday_str:
        :return:
        birthday or BirthdayValidationError
        '''
        if re.match(r'^[0-9]{4}/[0-9]{2}/[0-9]{2}$',birthday_str):
            year, month, day = map(int, birthday_str.split('/'))
            if not 1300 <= year <= 1390:
                return custom_exceptions.BirthdayValidationError()
            elif not 1 <= month <= 12:
                return custom_exceptions.BirthdayValidationError()
            elif 1 <= month <= 6 and not 1 <= day <= 31:
                return custom_exceptions.BirthdayValidationError()
            elif 7 <= month <= 11 and not 1 <= day <= 30:
                return custom_exceptions.BirthdayValidationError()
            elif month == 12 and not 1 <= day <= 29:
                return custom_exceptions.BirthdayValidationError()
            return birthday_str
        else:
            return custom_exceptions.BirthdayValidationError()
