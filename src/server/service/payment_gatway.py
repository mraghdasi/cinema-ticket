from datetime import datetime, date
from enum import Enum

from src.server.models.bank_account import UserBankAccount
from src.server.models.user import User
from src.utils.custom_exceptions import exception_log
from src.utils.utils import hash_string


class PaymentType(Enum):
    DEPOSIT_CARD = 'deposit_card'
    WITHDRAW_CARD = 'withdraw_card'
    TRANSFER = 'transfer'


def validate_user(user_id: int):
    """
   This function is used to validate the card number.

   Args:
       card_number (str): The card number of the user.
       msg (str): The message to be displayed in case of an error.

   Returns:
       None

   Raises:
       Exception: If the card number is not valid.

   """

    user = User.objects.read(f'id={user_id}')

    if len(user) == 0:
        raise Exception(f'User_id = {user_id} , Not Found')


def validate_card_number(card_number: str, msg: str):
    """
   This function is used to validate the card number.

   Args:
       card_number (str): The card number of the user.
       msg (str): The message to be displayed in case of an error.

   Returns:
       None

   Raises:
       Exception: If the card number is not valid.

   """

    card_result = UserBankAccount.objects.read(f'card_number="{card_number}"')

    if len(card_result) == 0:
        raise Exception(f'{msg} Card Number = {card_number} , Not Found')

    card_expire = str(card_result[0].expire_date)
    expiration_date = datetime.strptime(card_expire, "%Y-%m-%d").date()
    now = date.today()

    if expiration_date < now:
        raise Exception(f'{msg} Card Number = {card_number} , Expired')


def validate_card_number_amount(card_number: str, amount: int):
    """
    This function is used to validate the available balance of a card.

    Args:
        card_number (str): The card number of the user.
        amount (int): The amount of the withdrawal.

    Returns:
        None

    Raises:
        Exception: If the available balance is not sufficient.

    """

    card_result = UserBankAccount.objects.read(f'card_number="{card_number}"')[0]
    withdraw_able_card_amount = card_result.amount - card_result.minimum_amount

    if withdraw_able_card_amount < amount:
        raise Exception(f'Card Number = {card_number} , Cannot Withdraw more than {withdraw_able_card_amount}')


def validate_card_number_security(card_number: str, password: str, svv2: str):
    """
    This function is used to validate the security code of a card.

    Args:
        card_number (str): The card number of the user.
        password (str): The password of the user.
        svv2 (str): The cvv2 of the user.

    Returns:
        None

    Raises:
        Exception: If the security code is not valid.

    """

    card_result = UserBankAccount.objects.read(f'card_number="{card_number}"')[0]
    password = hash_string(password)
    cvv2 = hash_string(svv2)

    if card_result.password != password or card_result.cvv2 != cvv2:
        raise Exception(f'Card Number = {card_number} , Password Or CVV2 Not Valid')


def validate_same_card_number(origin_card_number: str, destination_card_number: str):
    if origin_card_number == destination_card_number:
        raise Exception(f'Origin Card Number = {origin_card_number} and Destination Card Number = {destination_card_number} are same')


@exception_log()
def payment_gateway(payType: PaymentType,
                    origin_user_id: int,
                    origin_card_number: str,
                    password: str,
                    cvv2: str,
                    amount: int,
                    destination_user_id=None,
                    destination_card_number=None):
    """
    This function is used to process payments.

    Args:
        payType (PaymentType): The type of payment.
        origin_user_id (int): The id of the origin user.
        origin_card_number (str): The card number of the origin user.
        password (str): The password of the origin user.
        cvv2 (str): The cvv2 of the origin user.
        amount (int): The amount of the payment.
        destination_user_id (int, optional): The id of the destination user.
        destination_card_number (str, optional): The card number of the destination user.

    Returns:
        None

    Raises:
        Exception: If any of the parameters are invalid.

    """

    validate_user(origin_user_id)
    validate_card_number(origin_card_number, 'Origin')
    validate_card_number_security(origin_card_number, password, cvv2)
    origin_card_result = UserBankAccount.objects.read(f'card_number="{origin_card_number}"')[0]

    if payType.value == PaymentType.DEPOSIT_CARD.value:
        UserBankAccount.objects.update({'amount': origin_card_result.amount + amount}, f'id="{origin_card_result.id}"')
    elif payType.value == PaymentType.TRANSFER.value:
        validate_user(destination_user_id)
        validate_card_number(destination_card_number, 'Destination')
        validate_card_number_amount(origin_card_number, amount)
        validate_same_card_number(origin_card_number, destination_card_number)

        destination_card_result = UserBankAccount.objects.read(f'card_number="{destination_card_number}"')[0]
        UserBankAccount.objects.update({'amount': destination_card_result.amount + amount}, f'id="{destination_card_result.id}"')
        UserBankAccount.objects.update({'amount': origin_card_result.amount - amount}, f'id="{origin_card_result.id}"')

# payment_gateway(PaymentType.TRANSFER, 1, '1234123412341234', 'mraghdasi', '4321', 2000, 1, '2345670432367890')
# payment_gateway(PaymentType.DEPOSIT_CARD,1, '4567567845673456', hash_string('457457'), hash_string('5685'), 10000)
