from datetime import datetime, date, timedelta
from hmac import compare_digest

from src.server.models.bank_account import UserBankAccount
from src.server.models.cinema_sans import CinemaSans
from src.server.models.comment import Comment
from src.server.models.film import Film
from src.server.models.film_rate import FilmRate
from src.server.models.hall import Hall
from src.server.models.package import Package
from src.server.models.subscription import Subscription
from src.server.models.ticket import Ticket
from src.server.models.user import User
from src.utils.custom_exceptions import DBError
from src.utils.transaction import set_transaction_log


def login_required(func):
    def wrapper(request):
        if request.session.user:
            return func(request)
        else:
            def login_required_error():
                return {'msg': 'Login Required', 'status_code': 401}

            return login_required_error()

    return wrapper


def do_login(request):
    payload = request.payload
    try:
        user = User.objects.read(f'username="{payload["username"]}"')
        if user:
            user = user[0]
            if compare_digest(user.password, payload['password']):
                request.session.user = user
                User.objects.update({'is_logged_in': 1, 'last_login': datetime.now().isoformat()}, f"id={user.id}")
                return {'user': {k: v if type(v) not in [date, datetime] else v.strftime('%Y-%m-%d') for k, v in
                                 vars(user).items()}, 'status_code': 200}
            else:
                return {'msg': 'Password Not Correct', 'status_code': 400}
        else:
            return {'msg': 'User Not Found', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def register(request):
    payload = request.payload
    try:
        try:
            user = User.objects.create(**payload)
            request.session.user = user
            User.objects.update({'is_logged_in': 1}, f"id={user.id}")

            return {'user': {k: v if type(v) not in [date, datetime] else v.strftime('%Y-%m-%d') for k, v in
                             vars(user).items()}, 'status_code': 200}
        except DBError:
            return {'msg': 'Duplication Error', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def register_cards(request):
    payload = request.payload
    try:
        try:
            payload['user_id'] = request.session.user.id
            UserBankAccount.objects.create(**payload)
            return {'status_code': 200}
        except DBError:
            return {'msg': 'Duplication Error', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def _convert_not_serializable(v):
    if type(v) == timedelta:
        return str(v)
    else:
        return v.strftime("%A")


def get_movies(request):
    try:
        films = Film.objects.read()
        for film in films:
            film_sans = CinemaSans.objects.read(f'film_id={film.id}')
            film.sans = [
                {k: v if type(v) not in [date, timedelta] else _convert_not_serializable(v) for (k, v) in
                 vars(sans).items()} for sans in film_sans]

        return {'payload': [vars(film) for film in films], 'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def add_ticket(request):
    payload = request.payload
    try:
        ticket = Ticket.objects.create(payload['sans_id'], request.session.user.id, payload['sit'])
        return {'payload': vars(ticket), 'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def _convert_not_serializable2(v):
    if type(v) == timedelta:
        return str(v)
    else:
        return v.strftime("%Y-%m-%d")


def check_seats(request):
    payload = request.payload
    try:
        tickets_of_cinema_sans = CinemaSans.objects.query(f'''
            SELECT * FROM ticket
            JOIN cinema_sans cs ON cs.id = ticket.cinema_sans_id
            WHERE cs.id = {payload['sans_id']}
        ''', fetch=True)
        tickets_of_cinema_sans = [
            {k: v if type(v) not in [datetime, date, timedelta] else _convert_not_serializable2(v) for (k, v) in
             vars(ticket).items()} for ticket in tickets_of_cinema_sans]
        hall = Hall.objects.read(f"id={payload['hall_id']}")[0]
        return {'payload': {'sans_tickets': tickets_of_cinema_sans, 'hall': vars(hall)}, 'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def check_tickets(request):
    try:
        tickets_of_user = Ticket.objects.query(f"""SELECT ticket.id as id,
           cinema_sans_id,
           user_id,
           sit_number,
           premiere_date,
           start_time,
           end_time,
           film_id,
           hall_id,
           price,
           title,
           min_age
            FROM ticket
                     JOIN cinema_sans cs on ticket.cinema_sans_id = cs.id
                     JOIN film f on cs.film_id = f.id
            WHERE user_id = {request.session.user.id}
            """, fetch=True)
        tickets_of_user = [
            {k: v if type(v) not in [datetime, date, timedelta] else _convert_not_serializable2(v) for (k, v) in
             vars(ticket).items()} for ticket in tickets_of_user]
        return {'payload': tickets_of_user, 'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def cancel_ticket(request):
    payload = request.payload
    try:
        Ticket.objects.delete(f"id={payload['ticket_id']} AND user_id={request.session.user.id}")
        return {'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def buy_subscription(request):
    payload = request.payload
    try:
        if len(Subscription.objects.read(
                f"user_id={request.session.user.id} AND expire_at > {datetime.now().strftime('%Y-%m-%d')}")) == 0:
            package = Package.objects.read(f"title=\"{payload['user_package']}\"")[0]
            subscription = Subscription.objects.create(request.session.user.id, package.id,
                                                       (datetime.now() + timedelta(days=31)).strftime('%Y-%m-%d'))
        else:
            package = Package.objects.read(f"title=\"{payload['user_package']}\"")[0]
            subscription = Subscription.objects.update({"package_id": package.id,
                                                        "expire_at": (datetime.now() + timedelta(days=31)).strftime(
                                                            '%Y-%m-%d')},
                                                       f'user_id={request.session.user.id}')

        return {'subscription': {k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for k, v in
                                 vars(subscription).items()},
                'package': vars(package),
                'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def check_subscription(request):
    try:
        subscriptions = Subscription.objects.read(
            f"user_id={request.session.user.id} AND expire_at > {datetime.now().strftime('%Y-%m-%d')}")
        if len(subscriptions) == 0:
            package = Package.objects.read('title="Bronze"')[0]
        else:
            package = Package.objects.read(f'id={subscriptions[0].package_id}')[0]
        return {'package': vars(package), 'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def get_cards(request):
    try:
        cards = UserBankAccount.objects.read(f'user_id={request.session.user.id}')
        card_dict = {}
        for card in cards:
            card_dict[card.title] = {'id': card.id, 'card_number': card.card_number, 'cvv2': card.cvv2,
                                     'password': card.password, 'expire_date': card.expire_date.strftime('%Y-%m-%d'),
                                     'amount': card.amount,
                                     'minimum_amount': card.minimum_amount}
        if len(card_dict) != 0:
            return {'cards': card_dict, 'status_code': 200}
        return {'msg': 'You Have No Cards In Our DataBase', 'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def check_db_for_transfer(request):
    payload = request.payload
    try:
        destination_card = UserBankAccount.objects.read(f'card_number={payload["destination_card"]}')
        if destination_card:
            # print(vars(destination_card[0]).items())
            return {'destination_card_obj': {k: v if type(v) != date else v.strftime('%Y-%m-%d') for (k, v) in
                                             vars(destination_card[0]).items()},
                    'status_code': 200}
        else:
            return {'msg': 'Destination Card Is Not In Our DataBase', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def do_transfer(request):
    payload = request.payload
    try:
        selected_card = UserBankAccount.objects.update({'amount': f'{payload["selected_card"]["amount"]}'},
                                                       f'card_number={payload["selected_card"]["card_number"]}')
        destination_card = UserBankAccount.objects.update({'amount': f'{payload["destination_card"]["amount"]}'},
                                                          f'card_number={payload["destination_card"]["card_number"]}')
        if selected_card and destination_card:
            return {'status_code': 200}
        else:
            return {'msg': 'Wrong Selected Card or Destination Card Info', 'status_code': 400}
    except DBError:
        return {'msg': 'Error in DataBase', 'status_code': 400}

    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def do_card_op(request):
    payload = request.payload
    try:
        selected_card_op = UserBankAccount.objects.update({'amount': f'{payload["selected_card"]["amount"]}'},
                                                          f'card_number={payload["selected_card"]["card_number"]}')
        if selected_card_op:
            return {'status_code': 200}
        else:
            return {'msg': 'Wrong Card Info', 'status_code': 400}
    except DBError:
        return {'msg': 'Error in DataBase', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def get_movie_rating(request):
    payload = request.payload
    try:
        rates = [rate.rate for rate in FilmRate.objects.read(f"film_id={payload['id']}")]
        if len(rates):
            film_rating = sum(rates) / len(rates)
        else:
            film_rating = 0
        return {'payload': film_rating, 'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def get_movie_comments(request):
    payload = request.payload
    try:
        comments = Comment.objects.read(f"film_id={payload['id']}")
        return {'comments': [{k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for k, v in
                              vars(comment).items()} for comment in comments],
                'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def add_comment(request):
    payload = request.payload
    try:
        comment = Comment.objects.create(**{'description': payload['description'], 'film_id': payload['movie_id'],
                                            'user_id': request.session.user.id})
        return {'comment': {k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for k, v in
                            vars(comment).items()},
                'status_code': 200}
    except DBError:
        return {'msg': 'Error in Database', 'status_code': 400}

    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def get_user_comments(request):
    payload = request.payload
    try:
        comments = Comment.objects.read(f"user_id={request.session.user.id} AND film_id={payload['movie_id']}")
        return {'comments': [{k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for k, v in
                              vars(comment).items()} for comment in comments],
                'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def delete_comment(request):
    payload = request.payload
    try:
        Comment.objects.delete(f"user_id={request.session.user.id} AND id={payload['comment_id']}")
        return {'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def wallet_deposit(request):
    payload = request.payload
    try:
        amount = int(payload['amount'])
        transaction_log_type = payload['transaction_log_type']
        user = request.session.user
        user_updated = User.objects.update({'balance': amount + user.balance}, f'id="{user.id}"')[0]
        set_transaction_log(amount, transaction_log_type, user.username)
        request.session.user = user_updated
        return {'msg': f'Your Wallet is successfully updated. Current Balance : {user_updated.balance}',
                'status_code': 200}
    except DBError:
        return {'msg': 'Error in Database', 'status_code': 400}

    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def wallet_withdraw(request):
    payload = request.payload
    try:
        amount = payload['amount']
        transaction_log_type = payload['transaction_log_type']
        user = request.session.user
        discount = 0
        if payload.get('operation', None) == 'ticket':
            user_birthday_month = user.birthday.month
            user_birthday_day = user.birthday.day
            discount = 0.5 if datetime.today().month == user_birthday_month and datetime.today().day == user_birthday_day else 0
        actual_amount = amount - (amount * discount)

        if user.balance >= actual_amount:
            user_updated = User.objects.update({'balance': user.balance - actual_amount}, f'id="{user.id}"')[0]
            set_transaction_log(-amount, transaction_log_type, user.username)
            request.session.user = user_updated
            return {
                'msg': f'Your Wallet is  successfully updated. Current Balance. Current Balance : {user_updated.balance}',
                'status_code': 200}
        else:
            return {'msg': 'Your Balance Is Not Enough Please Charge Your Wallet', 'status_code': 400}

    except DBError:
        return {'msg': 'Error in Database', 'status_code': 400}

    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def update_comment(request):
    payload = request.payload
    try:

        comments = Comment.objects.update({'description': payload['new_description']},
                                          f"user_id={request.session.user.id} AND id={payload['comment_id']}")
        if comments:
            return {'status_code': 200}
        else:
            return {'msg': 'Wrong Comment Id', 'status_code': 400}
    except DBError:
        return {'msg': 'Error in Database', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def add_comment_reply(request):
    payload = request.payload
    try:
        comment = Comment.objects.create(**{'description': payload['description'], 'film_id': payload['movie_id'],
                                            'user_id': request.session.user.id, 'reply_to': payload['reply_to']})
        return {'comment': {k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for k, v in
                            vars(comment).items()},
                'status_code': 200}
    except DBError:
        return {'msg': 'Error in Database', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def user_modification(request):
    payload = request.payload
    try:
        user_updated = User.objects.update(payload, f'id={request.session.user.id}')[0]
        request.session.user = user_updated
        return {'status_code': 200}
    except DBError:
        return {'msg': 'Error in Database', 'status_code': 400}

    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def add_rate(request):
    payload = request.payload
    try:
        rate = FilmRate.objects.create(**{'rate': payload['rate'], 'film_id': payload['movie_id'],
                                          'user_id': request.session.user.id})
        return {'rate': {k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for k, v in
                         vars(rate).items()},
                'status_code': 200}
    except DBError:
        return {'msg': 'Duplicate Rate Error', 'status_code': 400}

    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def get_user_rates(request):
    payload = request.payload
    try:
        rates = FilmRate.objects.read(f"user_id={request.session.user.id} AND film_id={payload['movie_id']}")
        return {'rates': [{k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for k, v in
                           vars(rate).items()} for rate in rates],
                'status_code': 200}
    except DBError:
        return {'msg': 'Error in Database', 'status_code': 400}

    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def delete_rate(request):
    payload = request.payload
    try:
        FilmRate.objects.delete(f"user_id={request.session.user.id} AND id={payload['rate_id']}")
        return {'status_code': 200}
    except DBError:
        return {'msg': 'Error in Database', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def update_rate(request):
    payload = request.payload
    try:
        FilmRate.objects.update({'rate': payload['new_rate']},
                                f"user_id={request.session.user.id} AND id={payload['rate_id']}")
        return {'status_code': 200}
    except DBError:
        return {'msg': 'Error in Database', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def get_movie_rates(request):
    payload = request.payload
    try:
        rates = FilmRate.objects.read(f"film_id={payload['id']}")
        return {'rates': [{k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for k, v in
                           vars(rate).items()} for rate in rates],
                'status_code': 200}
    except DBError:
        return {'msg': 'Error in Database', 'status_code': 400}

    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


def get_packages(request):
    try:
        packages = Package.objects.read()
        return {'packages': [{k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for k, v in
                              vars(package).items()} for package in packages],
                'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def show_profile(request):
    try:
        profile = {k: v if type(v) not in [datetime, date, timedelta] else v.strftime('%Y-%m-%d') for (k, v) in
                   vars(request.session.user).items()}
        return {'user': profile, 'status_code': 200}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def update_cards(request):
    payload = request.payload
    try:
        UserBankAccount.objects.update({k: v if type(v) not in [date] else v.strftime('%Y-%m-%d')
                                        for (k, v) in payload.items()}, f'id={payload["id"]}')
        return {'status_code': 200}
    except DBError:
        return {'status_code': 400}
    except Exception as e:
        return {'status_code': 500}


def add_movie(request):
    payload = request.payload
    try:
        film = Film.objects.create(**{'title': payload['title'], 'min_age': payload['min_age']})
        return {'film': {k: v if type(v) not in [date, datetime, timedelta] else v.strftime('%Y-%m-%d')
                         for (k, v) in vars(film).items()}, 'status_code': 200}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def delete_movie(request):
    payload = request.payload
    try:
        Film.objects.delete(f"id={payload['movie_id']}")
        return {'status_code': 200}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def update_movie(request):
    payload = request.payload
    try:
        Film.objects.update(payload['fields'], f"id={payload['movie_id']}")
        return {'status_code': 200}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def get_movie_sans(request):
    payload = request.payload
    try:
        sansses = CinemaSans.objects.query(f'''
                    SELECT cinema_sans.id,
                   premiere_date,
                   start_time,
                   end_time,
                   film_id,
                   hall_id,
                   price,
                   title,
                   capacity
            FROM cinema_sans
            JOIN hall ha ON ha.id = cinema_sans.hall_id
            WHERE film_id = {payload['movie_id']}''', fetch=True)
        return {
            'sansses': [
                {k: v if type(v) not in [datetime, date, timedelta] else _convert_not_serializable2(v) for (k, v) in
                 vars(sans).items()} for sans in sansses], 'status_code': 200}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def get_halls(request):
    payload = request.payload
    try:
        halls = Hall.objects.read()
        return {
            'halls': [
                {k: v if type(v) not in [datetime, date, timedelta] else _convert_not_serializable2(v) for (k, v) in
                 vars(hall).items()} for hall in halls], 'status_code': 200}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def add_sans(request):
    payload = request.payload
    try:
        CinemaSans.objects.create(**payload)
        return {'status_code': 200}
    except DBError:
        return {'msg': 'Invalid Payload', 'status_code': 400}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def delete_sans(request):
    payload = request.payload
    try:
        CinemaSans.objects.delete(f"id={payload['sans_id']}")
        return {'status_code': 200}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def update_sans(request):
    payload = request.payload
    try:
        sans = CinemaSans.objects.update(payload['data'], f"id={payload['sans_id']}")[0]
        return {
            'sans': {k: v if type(v) not in [datetime, date, timedelta] else _convert_not_serializable2(v) for (k, v) in
                     vars(sans).items()}, 'status_code': 200}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def add_hall(request):
    payload = request.payload
    try:
        Hall.objects.create(**payload)
        return {'status_code': 200}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def delete_hall(request):
    payload = request.payload
    try:
        Hall.objects.delete(f"id={payload['hall_id']}")
        return {'status_code': 200}
    except DBError:
        return {'msg': 'Can Not Delete Hall Because Existing Relation With Other Entities', 'status_code': 400}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}


def update_hall(request):
    payload = request.payload
    try:
        hall = Hall.objects.update(payload['data'], f"id={payload['hall_id']}")[0]
        return {
            'hall': {k: v if type(v) not in [datetime, date, timedelta] else _convert_not_serializable2(v) for (k, v) in
                     vars(hall).items()}, 'status_code': 200}
    except Exception as e:
        return {'msg': 'server Error', 'status_code': 500}
