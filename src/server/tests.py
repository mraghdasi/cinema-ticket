import unittest
from unittest.mock import MagicMock

from src.server.models.user import User
from src.server.views import do_login, register, register_cards
from src.utils.utils import hash_string


class TestDoLogin(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()

    def test_do_login_wrong_username(self):
        self.request.payload = {'username': 'soroush223132', 'password': 'asdasadsd'}
        self.request.session.user = None

        self.assertEqual(do_login(self.request)['msg'], 'User Not Found')

    def test_do_login_wrong_password(self):
        self.request.payload = {'username': 'aA1', 'password': 'asdasadsd'}
        self.request.session.user = None

        self.assertEqual(do_login(self.request)['msg'], 'Password Not Correct')

    def test_do_login_valid_data(self):
        self.request.payload = {'username': 'aA1', 'password': hash_string('aaAA!!11')}
        self.request.session.user = None
        self.response = do_login(self.request)
        self.assertEqual(self.response['status_code'], 200)


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()

    def test_register_not_complete_payload(self):
        self.request.payload = {'username': 'soroush223132', 'password': 'asdasadsd', 'email': 'asdasadsd'}
        self.request.session.user = None

        self.assertEqual(register(self.request)['msg'], 'Server Error')

    def test_register_complete_payload(self):
        User.objects.delete('username="soroush223132"')
        self.request.payload = {'username': 'soroush223132', 'password': 'asdasadsd', 'email': 'asdasadsd',
                                'phone_number': '09390468833', 'birthday': '2021-02-03'}
        self.request.session.user = None

        self.assertEqual(register(self.request)['status_code'], 200)

    def test_register_complete_payload_duplicate(self):
        self.request.payload = {'username': 'soroush223132', 'password': 'asdasadsd', 'email': 'asdasadsd',
                                'phone_number': '09390468833', 'birthday': '2021-02-03'}
        self.request.session.user = None

        self.assertEqual(register(self.request)['msg'], 'Duplication Error')


class TestRegisterCard(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.read('username="soroush223132"')[0]

    def test_register_card_not_complete_payload(self):
        self.request.payload = {'title': 'first_card'}

        self.assertEqual(register_cards(self.request)['msg'], 'Server Error')

    def test_register_card_complete_payload(self):
        self.request.payload = {'title': 'first_card', 'cvv2': '111', 'password': hash_string('1234'),
                                'card_number': '01234567890123456', 'expire_date': '2025-02-03'}

        self.assertEqual(register_cards(self.request)['status_code'], 200)

    def test_register_complete_payload_duplicate(self):
        self.request.payload = {'title': 'first_card', 'cvv2': '111', 'password': hash_string('1234'),
                                'card_number': '01234567890123456', 'expire_date': '2025-02-03'}

        self.assertEqual(register_cards(self.request)['msg'], 'Duplication Error')


if __name__ == '__main__':
    unittest.main()
