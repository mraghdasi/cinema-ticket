import re

from validators import email

from src.utils.custom_exceptions import UsernameValidationError, EmailValidationError, PhoneNumberValidationError


class Validator:
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
            pass
            # return UsernameValidationError()

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
            raise EmailValidationError()

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
                raise PhoneNumberValidationError()
        else:
            return None
