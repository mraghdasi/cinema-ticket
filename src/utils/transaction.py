import datetime
import logging
from enum import Enum

from src.utils.custom_exceptions import exception_log


class TransactionType(Enum):
    DEPOSIT_WALLET = 'deposit_wallet'
    WITHDRAW_WALLET = 'withdraw_wallet'
    DEPOSIT_CARD = 'deposit_card'
    WITHDRAW_CARD = 'withdraw_card'
    TRANSFER = 'transfer'
    BUY_PACKAGE = 'buy_package'
    BUY_TICKET = 'buy_ticket'
    CANCEL_TICKET = 'cancel_ticket'


@exception_log()
def set_transaction_log(amount: int, transaction_type: str, username: str, origin_card_number=None, destination_card_number=None):
    """
    Logs a transaction to a file.

    Args:
        origin_card_number (str): The card number of the customer.
        destination_card_number (str): The card number of the customer.
        amount (int): The amount of the transaction.
        transaction_type (TransactionType): The type of transaction.
        username (str): The username of the customer.

    """
    if int(amount) == 0:
        return

    logging.basicConfig(filename='../logs/transaction-logs.txt', level=logging.INFO)
    logging.info(
        f' Username : {username} {f"| Origin Card Number : {origin_card_number}" if origin_card_number else ""} '
        f'{f"| Destination Card Number : {destination_card_number}" if destination_card_number else ""}  '
        f'| Amount : {amount} | Transaction Type : {transaction_type} | DateTime : {datetime.datetime.now()}')

# set_transaction_log(10000, TransactionType.BUY_TICKET.value, 'mraghdasi')
