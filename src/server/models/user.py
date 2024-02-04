from datetime import date
from datetime import datetime

# from src.utils.custom_exceptions import NewPasswordsNotSame
# from src.utils.custom_exceptions import UserPasswordNotCorrect
from src.db.db_operations import Manager


class User:
    """
        Class To Make User Instances, It's a Basic User Without Any Specification.
    """
    username: str
    email: str
    phone_number: str
    password: str
    birthday: date
    last_login: None
    created_at: datetime
    balance: int
    role: int
    is_logged_in: int
    objects: object

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))

    def __init__(self, username, email, phone_number, password, birthday, **kwargs):
        """
        Initialize Instance (Constructor Method)
        """
        # validate_username = Validator.validate(username, (Validator.username_validator,))
        # if isinstance(validate_username, bool):
        #     self.username = username
        # else:
        #     raise Exception(validate_username)
        #
        # validate_email = Validator.validate(email, (Validator.email_validator,))
        # if isinstance(validate_email, bool):
        #     self.email = email
        # else:
        #     raise Exception(validate_email)
        #
        # validate_phone_number = Validator.validate(phone_number, (Validator.phone_number_validator,))
        # if isinstance(validate_phone_number, bool):
        #     self.phone_number = phone_number
        # else:
        #     raise Exception(validate_phone_number)

        # validate_password = Validator.validate(password, (Validator.password_validator,))
        # if isinstance(validate_password, bool):
        #     self.password = hash_string(password)
        # else:
        #     raise Exception(validate_password)

        # validate_birthday = Validator.validate(birthday, (Validator.birthday_format_validator,))
        # if isinstance(validate_birthday, bool):
        #     self.birthday = birthday
        # else:
        #     raise Exception(validate_birthday)
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.birthday = birthday
        self.role = 1
        self.is_logged_in = 0
        self.balance = 0
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'Username: {self.username} | Email: {self.email} | Role: {self.role}'

    # def change_password(self, password, new_password, confirm_new_password):
    #     """
    #     Change Password Of User, If New Password And Confirm New Password Are The Same, and Password is correct
    #     Updates User Password to New Password
    #     :param password:
    #     :param new_password:
    #     :param confirm_new_password:
    #     :return:
    #         True Or Raise Exception
    #     """
    #     if compare_digest(new_password, confirm_new_password):
    #         hashed_password = hash_string(password)
    #         user = self.read(
    #             **{'columns': '*', 'condition': f'username = {self.username} AND password = {hashed_password}'})
    #         if user:
    #             validate_password = Validator.validate(
    #                 new_password, (Validator.password_validator,))
    #             if isinstance(validate_password, bool):
    #                 hashed_new_password = hash_string(new_password)
    #                 self.password = hashed_new_password
    #                 self.update(
    #                     **{'columns': f'password = {hashed_new_password}', 'condition': f'id = {user.id}'})
    #                 return True
    #             else:
    #                 raise Exception(validate_password)
    #         else:
    #             return str(UserPasswordNotCorrect())
    #     else:
    #         return str(NewPasswordsNotSame())

    def set_user_logged_in(self):
        self.is_logged_in = 1

    def set_user_logged_out(self):
        self.is_logged_in = 0


User.set_manager()
