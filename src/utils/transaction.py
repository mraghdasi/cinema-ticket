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


@exception_log()
def set_transaction_log(card_number: str, amount: int, transaction_type: TransactionType, username: str):
    """
    Logs a transaction to a file.

    Args:
        card_number (str): The card number of the customer.
        amount (int): The amount of the transaction.
        transaction_type (TransactionType): The type of transaction.
        username (str): The username of the customer.

    Raises:
        Exception: If the transaction type is not valid.

    """

    if not isinstance(transaction_type, TransactionType):
        raise Exception(f'Invalid Transaction Type: {transaction_type}')

    logging.basicConfig(filename='../logs/transaction-logs.txt', level=logging.INFO)
    logging.info(f' Username : {username} | Card Number : {card_number} | Amount : {amount} | Transaction Type : {transaction_type.value} | DateTime : {datetime.datetime.now()}')

# set_transaction_log('4574584', 10000, TransactionType.BUY_TICKET, 'mraghdasi')
