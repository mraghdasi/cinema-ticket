from datetime import datetime, date, timedelta
from hmac import compare_digest

from src.server.models.cinema_sans import CinemaSans
from src.server.models.film import Film
from src.server.models.hall import Hall
from src.server.models.package import Package
from src.server.models.subscription import Subscription
from src.server.models.ticket import Ticket
from src.server.models.user import User
from src.utils.custom_exceptions import DBError


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
            return {'user': {k: v if type(v) not in [date, datetime] else v.strftime('%Y-%m-%d') for k, v in
                             vars(user).items()}, 'status_code': 200}
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
            return {'subscription': {k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for k, v in
                                     vars(subscription).items()},
                    'package': vars(package),
                    'status_code': 200}
        else:
            return {'msg': 'You already have a subscription', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def check_subscription(request):
    try:
        subscriptions = Subscription.objects.read(f"user_id={request.session.user.id} AND expire_at > {datetime.now().strftime('%Y-%m-%d')}")
        if len(subscriptions) == 0:
            package = Package.objects.read('title="Bronze"')[0]
        else:
            package = Package.objects.read(f'id={subscriptions[0].package_id}')[0]
        return {'package': vars(package), 'status_code': 200}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}

# @login_required
# def show_profile(request):
#     data = {k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for (k, v) in
#             vars(request.session.user).items()}
#     data['status_code']: 200
#     return data
