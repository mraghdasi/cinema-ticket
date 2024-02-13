import unittest
from unittest.mock import MagicMock

from src.server.views import *
from src.utils.utils import hash_string


class TestDoLogin(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = None
        User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})

    def tearDown(self):
        User.objects.delete('username ="soroush223132"')

    def test_do_login_wrong_username(self):
        self.request.payload = {'username': 'soroushasddasas223132', 'password': 'asdasadsd'}

        self.assertEqual(do_login(self.request)['msg'], 'User Not Found')

    def test_do_login_wrong_password(self):
        self.request.payload = {'username': 'soroush223132', 'password': hash_string('dsasadawr')}

        self.assertEqual(do_login(self.request)['msg'], 'Password Not Correct')

    def test_do_login_valid_data(self):
        self.request.payload = {'username': 'soroush223132', 'password': hash_string('asdasadsd')}
        self.response = do_login(self.request)
        self.assertEqual(self.response['status_code'], 200)


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()

    def tearDown(self):
        User.objects.delete('username ="soroush223132"')

    def test_register_not_complete_payload(self):
        self.request.payload = {'username': 'soroush223132', 'password': 'asdasadsd', 'email': 'asdasadsd'}
        self.request.session.user = None

        self.assertEqual(register(self.request)['msg'], 'Server Error')

    def test_register_complete_payload(self):
        self.request.payload = {'username': 'soroush223132', 'password': 'asdasadsd', 'email': 'asdasadsd',
                                'phone_number': '09390468833', 'birthday': '2021-02-03'}
        self.request.session.user = None

        self.assertEqual(register(self.request)['status_code'], 200)

    def test_register_complete_payload_duplicate(self):
        self.request.payload = {'username': 'soroush223132', 'password': 'asdasadsd', 'email': 'asdasadsd',
                                'phone_number': '09390468833', 'birthday': '2021-02-03'}
        self.request.session.user = None
        register(self.request)
        self.assertEqual(register(self.request)['msg'], 'Duplication Error')


class TestRegisterCard(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})

    def tearDown(self):
        UserBankAccount.objects.delete('title ="first_card"')
        User.objects.delete('username ="soroush223132"')

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
        register_cards(self.request)
        self.assertEqual(register_cards(self.request)['msg'], 'Duplication Error')


class TestGetMovies(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        film1 = Film.objects.create('Film11', 20)
        film2 = Film.objects.create('Film22', 18)
        hall1 = Hall.objects.create('Hall11', 100)
        hall2 = Hall.objects.create('Hall22', 80)
        CinemaSans.objects.create('2024-03-02', '12:12:00', '14:00:00', film1.id, hall1.id, 5000)
        CinemaSans.objects.create('2024-03-03', '12:12:00', '14:00:00', film1.id, hall1.id, 5000)
        CinemaSans.objects.create('2024-03-02', '12:12:00', '14:00:00', film2.id, hall2.id, 5000)
        CinemaSans.objects.create('2024-03-03', '12:12:00', '14:00:00', film2.id, hall2.id, 5000)

    def tearDown(self):
        film1 = Film.objects.read('title="Film11"')[0]
        film2 = Film.objects.read('title="Film22"')[0]

        CinemaSans.objects.delete(f'film_id={film1.id}')
        CinemaSans.objects.delete(f'film_id={film2.id}')

        Film.objects.delete('title="Film11"')
        Film.objects.delete('title="Film22"')
        Hall.objects.delete('title="Hall11"')
        Hall.objects.delete('title="Hall22"')

    def test_get_movies(self):
        self.request.payload = {}

        self.assertEqual(get_movies(self.request)['status_code'], 200)


class TestAddTicket(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        film1 = Film.objects.create('Film11', 20)
        hall1 = Hall.objects.create('Hall11', 100)
        self.cinema_sans_1 = CinemaSans.objects.create('2024-03-02', '12:12:00', '14:00:00', film1.id, hall1.id, 5000)
        self.cinema_sans_2 = CinemaSans.objects.create('2024-03-03', '12:12:00', '14:00:00', film1.id, hall1.id, 5000)

    def tearDown(self):
        film1 = Film.objects.read('title="Film11"')[0]

        Ticket.objects.delete(f'user_id={self.request.session.user.id}')
        CinemaSans.objects.delete(f'film_id={film1.id}')

        Film.objects.delete('title="Film11"')
        Hall.objects.delete('title="Hall11"')
        User.objects.delete('username ="soroush223132"')

    def test_add_ticket_without_payload(self):
        self.request.payload = {}

        self.assertEqual(add_ticket(self.request)['status_code'], 500)

    def test_add_ticket_with_correct_payload(self):
        self.request.payload = {"sans_id": self.cinema_sans_1.id, 'sit': 50}

        self.assertEqual(add_ticket(self.request)['status_code'], 200)


class TestCheckSeats(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})

        self.film1 = Film.objects.create('Film11', 20)
        self.hall1 = Hall.objects.create('Hall11', 100)
        self.cinema_sans_1 = CinemaSans.objects.create('2024-03-02', '12:12:00', '14:00:00', self.film1.id,
                                                       self.hall1.id, 5000)
        self.ticket_1 = Ticket.objects.create(self.cinema_sans_1.id, self.request.session.user.id, 25)

    def tearDown(self):
        Ticket.objects.delete(f'id={self.ticket_1.id}')
        CinemaSans.objects.delete(f'film_id={self.film1.id}')

        Film.objects.delete(f'id="{self.film1.id}"')
        Hall.objects.delete(f'id="{self.hall1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_check_seats(self):
        self.request.payload = {}

        self.assertEqual(check_tickets(self.request)['status_code'], 200)


class TestCheckTickets(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.film1 = Film.objects.create('Film11', 20)
        self.hall1 = Hall.objects.create('Hall11', 100)
        self.cinema_sans_1 = CinemaSans.objects.create('2024-03-02', '12:12:00', '14:00:00', self.film1.id,
                                                       self.hall1.id, 5000)

    def tearDown(self):
        film1 = Film.objects.read('title="Film11"')[0]

        CinemaSans.objects.delete(f'film_id={film1.id}')

        Film.objects.delete('title="Film11"')
        Hall.objects.delete('title="Hall11"')

    def test_check_seats_without_payload(self):
        self.request.payload = {}

        self.assertEqual(check_seats(self.request)['status_code'], 500)

    def test_check_seats_with_correct_payload(self):
        self.request.payload = {"sans_id": self.cinema_sans_1.id, 'hall_id': self.hall1.id}

        self.assertEqual(check_seats(self.request)['status_code'], 200)


class TestCancelTicket(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})

        self.film1 = Film.objects.create('Film11', 20)
        self.hall1 = Hall.objects.create('Hall11', 100)
        self.cinema_sans_1 = CinemaSans.objects.create('2024-03-02', '12:12:00', '14:00:00', self.film1.id,
                                                       self.hall1.id, 5000)
        self.ticket_1 = Ticket.objects.create(self.cinema_sans_1.id, self.request.session.user.id, 25)

    def tearDown(self):
        Ticket.objects.delete(f'id={self.ticket_1.id}')
        CinemaSans.objects.delete(f'film_id={self.film1.id}')

        Film.objects.delete(f'id="{self.film1.id}"')
        Hall.objects.delete(f'id="{self.hall1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_cancel_ticket_without_payload(self):
        self.request.payload = {}

        self.assertEqual(cancel_ticket(self.request)['status_code'], 500)

    def test_cancel_ticket_with_correct_payload(self):
        self.request.payload = {"ticket_id": self.ticket_1.id}

        self.assertEqual(cancel_ticket(self.request)['status_code'], 200)


class TestBuySubscription(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})

    def tearDown(self):
        Subscription.objects.delete(f'user_id={self.request.session.user.id}')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_buy_subscription_without_payload(self):
        self.request.payload = {}

        self.assertEqual(buy_subscription(self.request)['status_code'], 500)

    def test_buy_subscription_with_correct_payload(self):
        self.request.payload = {"user_package": "Gold"}

        self.assertEqual(buy_subscription(self.request)['status_code'], 200)

    # def test_buy_subscription_with_correct_payload_duplicate(self):
    #     self.request.payload = {"user_package": "Gold"}
    #     buy_subscription(self.request)
    #     self.assertEqual(buy_subscription(self.request)['status_code'], 400)


class TestCheckSubscription(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})

    def tearDown(self):
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_check_subscription(self):
        self.request.payload = {}

        self.assertEqual(check_subscription(self.request)['status_code'], 200)


class TestGetCards(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})

    def tearDown(self):
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_get_cards(self):
        self.request.payload = {}

        self.assertEqual(get_cards(self.request)['status_code'], 200)


class TestCheckDbForTransfer(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.bank_account_1 = UserBankAccount.objects.create(
            **{'user_id': self.request.session.user.id, 'title': 'first_card', 'cvv2': '111',
               'password': hash_string('1234'),
               'card_number': '01234567890123456', 'expire_date': '2025-02-03'})

    def tearDown(self):
        UserBankAccount.objects.delete(f'id={self.bank_account_1.id}')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_check_db_for_transfer_without_payload(self):
        self.request.payload = {}

        self.assertEqual(check_db_for_transfer(self.request)['status_code'], 500)

    def test_check_db_for_transfer_with_wrong_payload(self):
        self.request.payload = {'destination_card': '51215151515'}

        self.assertEqual(check_db_for_transfer(self.request)['status_code'], 400)

    def test_check_db_for_transfer_with_correct_payload(self):
        self.request.payload = {'destination_card': self.bank_account_1.card_number}

        self.assertEqual(check_db_for_transfer(self.request)['status_code'], 200)


class TestDoTransfer(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.bank_account_1 = UserBankAccount.objects.create(
            **{'user_id': self.request.session.user.id, 'title': 'first_card', 'cvv2': '111',
               'password': hash_string('1234'),
               'card_number': '01234567890123456', 'expire_date': '2025-02-03'})
        self.bank_account_2 = UserBankAccount.objects.create(
            **{'user_id': self.request.session.user.id, 'title': 'second_card', 'cvv2': '111',
               'password': hash_string('4321'),
               'card_number': '01234567894132456', 'expire_date': '2025-02-03'})

    def tearDown(self):
        UserBankAccount.objects.delete(f'id={self.bank_account_1.id}')
        UserBankAccount.objects.delete(f'id={self.bank_account_2.id}')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_do_transfer_without_payload(self):
        self.request.payload = {}

        self.assertEqual(do_transfer(self.request)['status_code'], 500)

    def test_do_transfer_with_wrong_payload(self):
        self.request.payload = {'selected_card': {'amount': 'st00', 'card_number': self.bank_account_1.card_number},
                                'destination_card': {'amount': 'st00', 'card_number': self.bank_account_2.card_number}}

        self.assertEqual(do_transfer(self.request)['status_code'], 400)

    def test_do_transfer_with_wrong_card_number(self):
        self.request.payload = {'selected_card': {'amount': 5000, 'card_number': self.bank_account_1.card_number},
                                'destination_card': {'amount': 5000, 'card_number': 's12asd2ads215'}}

        self.assertEqual(do_transfer(self.request)['status_code'], 400)

    def test_do_transfer_with_correct_payload(self):
        self.request.payload = {'selected_card': {'amount': 5000, 'card_number': self.bank_account_1.card_number},
                                'destination_card': {'amount': 5000, 'card_number': self.bank_account_2.card_number}}

        self.assertEqual(do_transfer(self.request)['status_code'], 200)


class TestDoCardOp(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.bank_account_1 = UserBankAccount.objects.create(
            **{'user_id': self.request.session.user.id, 'title': 'first_card', 'cvv2': '111',
               'password': hash_string('1234'),
               'card_number': '01234567890123456', 'expire_date': '2025-02-03'})

    def tearDown(self):
        UserBankAccount.objects.delete(f'id={self.bank_account_1.id}')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_do_card_op_without_payload(self):
        self.request.payload = {}

        self.assertEqual(do_card_op(self.request)['status_code'], 500)

    def test_do_card_op_with_wrong_payload(self):
        self.request.payload = {'selected_card': {'amount': 'st00', 'card_number': self.bank_account_1.card_number}}

        self.assertEqual(do_card_op(self.request)['status_code'], 400)

    def test_do_card_op_with_wrong_card_number(self):
        self.request.payload = {'selected_card': {'amount': 5000, 'card_number': '625666262612'}}

        self.assertEqual(do_card_op(self.request)['status_code'], 400)

    def test_do_card_op_with_correct_payload(self):
        self.request.payload = {'selected_card': {'amount': 5000, 'card_number': self.bank_account_1.card_number}}

        self.assertEqual(do_card_op(self.request)['status_code'], 200)


class TestGetMovieRating(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.film1 = Film.objects.create('Film11', 20)

    def tearDown(self):
        Film.objects.delete(f'id="{self.film1.id}"')

    def test_get_movie_rating_without_payload(self):
        self.request.payload = {}

        self.assertEqual(get_movie_rating(self.request)['status_code'], 500)

    def test_get_movie_rating_with_correct_payload(self):
        self.request.payload = {'id': self.film1.id}

        self.assertEqual(get_movie_rating(self.request)['status_code'], 200)


class TestGetMovieComments(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.film1 = Film.objects.create('Film11', 20)

    def tearDown(self):
        Film.objects.delete(f'id="{self.film1.id}"')

    def test_get_movie_comments_without_payload(self):
        self.request.payload = {}

        self.assertEqual(get_movie_comments(self.request)['status_code'], 500)

    def test_get_movie_comments_with_correct_payload(self):
        self.request.payload = {'id': self.film1.id}

        self.assertEqual(get_movie_comments(self.request)['status_code'], 200)


class TestAddComment(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.film1 = Film.objects.create('Film11', 20)

    def tearDown(self):
        Comment.objects.delete(f'film_id="{self.film1.id}"')
        Film.objects.delete(f'id="{self.film1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_add_comment_without_payload(self):
        self.request.payload = {}

        self.assertEqual(add_comment(self.request)['status_code'], 500)

    def test_add_comment_with_wrong_film_id(self):
        self.request.payload = {'movie_id': '2515', 'description': 'adsdassaads'}

        self.assertEqual(add_comment(self.request)['status_code'], 400)

    def test_add_comment_with_correct_payload(self):
        self.request.payload = {'movie_id': self.film1.id, 'description': 'adsdassaads'}

        self.assertEqual(add_comment(self.request)['status_code'], 200)


class TestGetUserComments(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.film1 = Film.objects.create('Film11', 20)

    def tearDown(self):
        Film.objects.delete(f'id="{self.film1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_get_user_comments_without_payload(self):
        self.request.payload = {}

        self.assertEqual(get_user_comments(self.request)['status_code'], 500)

    def test_get_user_comments_with_wrong_film_id(self):
        self.request.payload = {'movie_id': '2515'}

        self.assertEqual(len(get_user_comments(self.request)['comments']), 0)

    def test_get_user_comments_with_correct_payload(self):
        self.request.payload = {'movie_id': self.film1.id}

        self.assertEqual(get_user_comments(self.request)['status_code'], 200)


class TestDeleteComment(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.film1 = Film.objects.create('Film11', 20)
        self.comment1 = Comment.objects.create(
            **{'description': 'sdasd', 'film_id': self.film1.id, 'user_id': self.request.session.user.id})

    def tearDown(self):
        Comment.objects.delete(f'film_id="{self.film1.id}"')
        Film.objects.delete(f'id="{self.film1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_delete_comment_without_payload(self):
        self.request.payload = {}

        self.assertEqual(delete_comment(self.request)['status_code'], 500)

    def test_delete_comment_with_correct_payload(self):
        self.request.payload = {'comment_id': self.comment1.id}

        self.assertEqual(delete_comment(self.request)['status_code'], 200)


class TestWalletDeposit(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})

    def tearDown(self):
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_wallet_deposit_without_payload(self):
        self.request.payload = {}

        self.assertEqual(wallet_deposit(self.request)['status_code'], 500)

    def test_wallet_deposit_with_wrong_payload(self):
        self.request.payload = {'amount': 'sadasad', 'transaction_log_type': 'deposit'}

        self.assertEqual(wallet_deposit(self.request)['status_code'], 500)

    def test_wallet_deposit_with_correct_payload(self):
        self.request.payload = {'amount': 1000, 'transaction_log_type': 'deposit'}

        self.assertEqual(wallet_deposit(self.request)['status_code'], 200)


class TestWalletWithdraw(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})

    def tearDown(self):
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_wallet_withdraw_without_payload(self):
        self.request.payload = {}

        self.assertEqual(wallet_withdraw(self.request)['status_code'], 500)

    def test_wallet_withdraw_with_wrong_payload(self):
        self.request.payload = {'amount': 'sadasad', 'transaction_log_type': 'withdraw'}

        self.assertEqual(wallet_withdraw(self.request)['status_code'], 500)

    def test_wallet_withdraw_with_correct_payload_not_enough_balance(self):
        self.request.payload = {'amount': 1000, 'transaction_log_type': 'withdraw'}

        self.assertEqual(wallet_withdraw(self.request)['status_code'], 400)

    def test_wallet_withdraw_with_correct_payload(self):
        self.request.payload = {'amount': 0, 'transaction_log_type': 'withdraw'}

        self.assertEqual(wallet_withdraw(self.request)['status_code'], 200)


class TestUpdateComment(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.film1 = Film.objects.create('Film11', 20)
        self.comment1 = Comment.objects.create(
            **{'description': 'sdasd', 'film_id': self.film1.id, 'user_id': self.request.session.user.id})

    def tearDown(self):
        Comment.objects.delete(f'film_id="{self.film1.id}"')
        Film.objects.delete(f'id="{self.film1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_update_comment_without_payload(self):
        self.request.payload = {}

        self.assertEqual(update_comment(self.request)['status_code'], 500)

    def test_update_comment_with_wrong_payload(self):
        self.request.payload = {'new_description': 'asddhasash', 'comment_id': '1565'}

        self.assertEqual(update_comment(self.request)['status_code'], 400)

    def test_update_comment_with_correct_payload(self):
        self.request.payload = {'new_description': 'asddhasash', 'comment_id': self.comment1.id}

        self.assertEqual(update_comment(self.request)['status_code'], 200)


class TestAddCommentReply(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.film1 = Film.objects.create('Film11', 20)
        self.comment1 = Comment.objects.create(
            **{'description': 'sdasd', 'film_id': self.film1.id, 'user_id': self.request.session.user.id})

    def tearDown(self):
        Comment.objects.delete(f'film_id="{self.film1.id}"')
        Film.objects.delete(f'id="{self.film1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_add_comment_reply_without_payload(self):
        self.request.payload = {}

        self.assertEqual(add_comment_reply(self.request)['status_code'], 500)

    def test_add_comment_reply_with_wrong_payload(self):
        self.request.payload = {'description': 'asddhasash', 'movie_id': '1565', 'reply_to': self.comment1.id}

        self.assertEqual(add_comment_reply(self.request)['status_code'], 400)

    def test_add_comment_reply_with_correct_payload(self):
        self.request.payload = {'description': 'asddhasash', 'movie_id': self.film1.id, 'reply_to': self.comment1.id}

        self.assertEqual(add_comment_reply(self.request)['status_code'], 200)


class TestUserModification(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.film1 = Film.objects.create('Film11', 20)
        self.comment1 = Comment.objects.create(
            **{'description': 'sdasd', 'film_id': self.film1.id, 'user_id': self.request.session.user.id})

    def tearDown(self):
        Comment.objects.delete(f'film_id="{self.film1.id}"')
        Film.objects.delete(f'id="{self.film1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_user_modification_without_payload(self):
        self.request.payload = {}

        self.assertEqual(user_modification(self.request)['status_code'], 400)

    def test_user_modification_with_wrong_payload(self):
        self.request.payload = {'username_data': 'test1'}

        self.assertEqual(user_modification(self.request)['status_code'], 400)

    def test_user_modification_with_correct_payload(self):
        self.request.payload = {'username': 'test1'}

        self.assertEqual(user_modification(self.request)['status_code'], 200)


class TestAddRate(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.film1 = Film.objects.create('Film11', 20)

    def tearDown(self):
        FilmRate.objects.delete(f'film_id="{self.film1.id}"')
        Film.objects.delete(f'id="{self.film1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_add_rate_without_payload(self):
        self.request.payload = {}

        self.assertEqual(add_rate(self.request)['status_code'], 500)

    def test_add_rate_with_wrong_payload(self):
        self.request.payload = {'rate': 10, 'movie_id': 'sadads'}

        self.assertEqual(add_rate(self.request)['status_code'], 400)

    def test_add_rate_with_correct_payload(self):
        self.request.payload = {'rate': 10, 'movie_id': self.film1.id}

        self.assertEqual(add_rate(self.request)['status_code'], 200)


class TestGetUserRates(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.film1 = Film.objects.create('Film11', 20)

    def tearDown(self):
        Film.objects.delete(f'id="{self.film1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_get_user_rates_without_payload(self):
        self.request.payload = {}

        self.assertEqual(get_user_rates(self.request)['status_code'], 500)

    def test_get_user_rates_with_wrong_payload(self):
        self.request.payload = {'movie_id': 'sadads'}

        self.assertEqual(get_user_rates(self.request)['status_code'], 400)

    def test_get_user_rates_with_correct_payload(self):
        self.request.payload = {'movie_id': self.film1.id}

        self.assertEqual(get_user_rates(self.request)['status_code'], 200)


class TestDeleteRate(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.film1 = Film.objects.create('Film11', 20)
        self.rate1 = FilmRate.objects.create(
            **{'film_id': self.film1.id, 'user_id': self.request.session.user.id, 'rate': 10})

    def tearDown(self):
        FilmRate.objects.delete(f'film_id="{self.film1.id}"')
        Film.objects.delete(f'id="{self.film1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_delete_rate_without_payload(self):
        self.request.payload = {}

        self.assertEqual(delete_rate(self.request)['status_code'], 500)

    def test_delete_rate_with_wrong_payload(self):
        self.request.payload = {'rate_id': 'sadads'}

        self.assertEqual(delete_rate(self.request)['status_code'], 400)

    def test_delete_rate_with_correct_payload(self):
        self.request.payload = {'rate_id': self.rate1.id}

        self.assertEqual(delete_rate(self.request)['status_code'], 200)


class TestUpdateRate(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.film1 = Film.objects.create('Film11', 20)
        self.rate1 = FilmRate.objects.create(
            **{'film_id': self.film1.id, 'user_id': self.request.session.user.id, 'rate': 10})

    def tearDown(self):
        FilmRate.objects.delete(f'film_id="{self.film1.id}"')
        Film.objects.delete(f'id="{self.film1.id}"')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_update_rate_without_payload(self):
        self.request.payload = {}

        self.assertEqual(update_rate(self.request)['status_code'], 500)

    def test_update_rate_with_wrong_payload(self):
        self.request.payload = {'rate_id': 'sadads', 'new_rate': 8}

        self.assertEqual(update_rate(self.request)['status_code'], 400)

    def test_update_rate_with_correct_payload(self):
        self.request.payload = {'rate_id': self.rate1.id, 'new_rate': 8}

        self.assertEqual(update_rate(self.request)['status_code'], 200)


class TestGetMovieRates(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.film1 = Film.objects.create('Film11', 20)

    def tearDown(self):
        Film.objects.delete(f'id="{self.film1.id}"')

    def test_get_movie_rates_without_payload(self):
        self.request.payload = {}

        self.assertEqual(get_movie_rates(self.request)['status_code'], 500)

    def test_get_movie_rates_with_wrong_payload(self):
        self.request.payload = {'id': 'sadads'}

        self.assertEqual(get_movie_rates(self.request)['status_code'], 400)

    def test_get_movie_rates_with_correct_payload(self):
        self.request.payload = {'id': self.film1.id}

        self.assertEqual(get_movie_rates(self.request)['status_code'], 200)


class TestShowProfile(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})

    def tearDown(self):
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_show_profile(self):
        self.request.payload = {}

        self.assertEqual(show_profile(self.request)['status_code'], 200)


class TestUpdateCards(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.session.user = User.objects.create(
            **{'username': 'soroush223132', 'password': hash_string('asdasadsd'), 'email': 'asdasadsd',
               'phone_number': '09390468833', 'birthday': '2021-02-03'})
        self.bank_account_1 = UserBankAccount.objects.create(
            **{'user_id': self.request.session.user.id, 'title': 'first_card', 'cvv2': '111',
               'password': hash_string('1234'),
               'card_number': '01234567890123456', 'expire_date': '2025-02-03'})

    def tearDown(self):
        UserBankAccount.objects.delete(f'id={self.bank_account_1.id}')
        User.objects.delete(f'id={self.request.session.user.id}')

    def test_update_cards_without_payload(self):
        self.request.payload = {}

        self.assertEqual(update_cards(self.request)['status_code'], 500)

    def test_update_cards_with_wrong_payload(self):
        self.request.payload = {'id': 'asddhasash'}

        self.assertEqual(update_cards(self.request)['status_code'], 400)

    def test_update_cards_with_correct_payload(self):
        self.request.payload = {'id': self.bank_account_1.id}

        self.assertEqual(update_cards(self.request)['status_code'], 200)


class TestAddMovie(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()

    def tearDown(self):
        Film.objects.delete(f'title="TEST_FILM1"')

    def test_add_movie_without_payload(self):
        self.request.payload = {}

        self.assertEqual(add_movie(self.request)['status_code'], 500)

    def test_add_movie_with_correct_payload(self):
        self.request.payload = {'min_age': 20, 'title': "TEST_FILM1"}

        self.assertEqual(add_movie(self.request)['status_code'], 200)


class TestDeleteMovie(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.film1 = Film.objects.create('Film11', 20)

    def tearDown(self):
        Film.objects.delete(f'id="{self.film1.id}"')

    def test_delete_movie_without_payload(self):
        self.request.payload = {}

        self.assertEqual(delete_movie(self.request)['status_code'], 500)

    def test_delete_movie_with_correct_payload(self):
        self.request.payload = {'movie_id': self.film1.id}

        self.assertEqual(delete_movie(self.request)['status_code'], 200)


class TestUpdateMovie(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.film1 = Film.objects.create('Film11', 20)

    def tearDown(self):
        Film.objects.delete(f'id="{self.film1.id}"')

    def test_update_movie_without_payload(self):
        self.request.payload = {}

        self.assertEqual(update_movie(self.request)['status_code'], 500)

    def test_update_movie_with_correct_payload(self):
        self.request.payload = {'movie_id': self.film1.id, 'fields': {'title': 'Film22'}}

        self.assertEqual(update_movie(self.request)['status_code'], 200)


class TestGetMovieSans(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.film1 = Film.objects.create('Film11', 20)
        self.hall1 = Hall.objects.create('Hall11', 100)
        self.cinema_sans_1 = CinemaSans.objects.create('2024-03-02', '12:12:00', '14:00:00', self.film1.id,
                                                       self.hall1.id, 5000)

    def tearDown(self):
        CinemaSans.objects.delete(f'film_id={self.film1.id}')
        Film.objects.delete(f'id="{self.film1.id}"')
        Hall.objects.delete(f'id="{self.hall1.id}"')

    def test_get_movie_sans_without_payload(self):
        self.request.payload = {}

        self.assertEqual(get_movie_sans(self.request)['status_code'], 500)

    def test_get_movie_sans_with_correct_payload(self):
        self.request.payload = {'movie_id': self.film1.id}

        self.assertEqual(get_movie_sans(self.request)['status_code'], 200)


class TestGetHalls(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.hall1 = Hall.objects.create('Hall11', 100)

    def tearDown(self):
        Hall.objects.delete(f'id="{self.hall1.id}"')

    def test_get_halls(self):
        self.request.payload = {}

        self.assertEqual(get_halls(self.request)['status_code'], 200)


class TestAddSans(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.film1 = Film.objects.create('Film11', 20)
        self.hall1 = Hall.objects.create('Hall11', 100)

    def tearDown(self):
        CinemaSans.objects.delete(f'film_id={self.film1.id}')
        Film.objects.delete(f'id="{self.film1.id}"')
        Hall.objects.delete(f'id="{self.hall1.id}"')

    def test_add_sans_without_payload(self):
        self.request.payload = {}

        self.assertEqual(add_sans(self.request)['status_code'], 500)

    def test_add_sans_with_correct_payload(self):
        self.request.payload = {'film_id': self.film1.id, 'hall_id': self.hall1.id, 'premiere_date': '2025-01-01',
                                'start_time': '10:10:10', 'end_time': '10:10:10', 'price': 15000,
                                }

        self.assertEqual(add_sans(self.request)['status_code'], 200)


class TestDeleteSans(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.film1 = Film.objects.create('Film11', 20)
        self.hall1 = Hall.objects.create('Hall11', 100)
        self.cinema_sans_1 = CinemaSans.objects.create('2024-03-02', '12:12:00', '14:00:00', self.film1.id,
                                                       self.hall1.id, 5000)

    def tearDown(self):
        CinemaSans.objects.delete(f'film_id={self.film1.id}')
        Film.objects.delete(f'id="{self.film1.id}"')
        Hall.objects.delete(f'id="{self.hall1.id}"')

    def test_delete_sans_without_payload(self):
        self.request.payload = {}
        self.assertEqual(delete_sans(self.request)['status_code'], 500)

    def test_delete_sans_with_correct_payload(self):
        self.request.payload = {'sans_id': self.cinema_sans_1.id}

        self.assertEqual(delete_sans(self.request)['status_code'], 200)


class TestUpdateSans(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.film1 = Film.objects.create('Film11', 20)
        self.hall1 = Hall.objects.create('Hall11', 100)
        self.cinema_sans_1 = CinemaSans.objects.create('2024-03-02', '12:12:00', '14:00:00', self.film1.id,
                                                       self.hall1.id, 5000)

    def tearDown(self):
        CinemaSans.objects.delete(f'film_id={self.film1.id}')
        Film.objects.delete(f'id="{self.film1.id}"')
        Hall.objects.delete(f'id="{self.hall1.id}"')

    def test_update_sans_without_payload(self):
        self.request.payload = {}
        self.assertEqual(update_sans(self.request)['status_code'], 500)

    def test_update_sans_with_correct_payload(self):
        self.request.payload = {'sans_id': self.cinema_sans_1.id, 'data': {'end_time': '18:00:00'}}

        self.assertEqual(update_sans(self.request)['status_code'], 200)


class TestAddHall(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()

    def tearDown(self):
        Hall.objects.delete(f'title="TESTHAll1"')

    def test_add_hall_without_payload(self):
        self.request.payload = {}
        self.assertEqual(add_hall(self.request)['status_code'], 500)

    def test_add_hall_with_correct_payload(self):
        self.request.payload = {'title': "TESTHAll1", 'capacity': 40}

        self.assertEqual(add_hall(self.request)['status_code'], 200)


class TestDeleteHall(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.hall1 = Hall.objects.create('Hall11', 100)

    def tearDown(self):
        Hall.objects.delete(f'id={self.hall1.id}')

    def test_delete_hall_without_payload(self):
        self.request.payload = {}
        self.assertEqual(delete_hall(self.request)['status_code'], 500)

    def test_delete_hall_with_correct_payload(self):
        self.request.payload = {'hall_id': self.hall1.id}

        self.assertEqual(delete_hall(self.request)['status_code'], 200)


class TestUpdateHall(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.hall1 = Hall.objects.create('Hall11', 100)

    def tearDown(self):
        Hall.objects.delete(f'id={self.hall1.id}')

    def test_update_hall_without_payload(self):
        self.request.payload = {}
        self.assertEqual(update_hall(self.request)['status_code'], 500)

    def test_update_hall_with_correct_payload(self):
        self.request.payload = {'hall_id': self.hall1.id, 'data': {'title': 'sdaasdas'}}

        self.assertEqual(update_hall(self.request)['status_code'], 200)


if __name__ == '__main__':
    unittest.main()
