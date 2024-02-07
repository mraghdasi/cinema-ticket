from datetime import datetime, date
from hmac import compare_digest

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
            print(user.password, payload['password'])
            if compare_digest(user.password, payload['password']):
                request.session.user = user
                return {'user': {k: v if type(v) not in [date, datetime] else v.strftime('%Y-%m-%d') for k, v in vars(user).items()}, 'status_code': 200}
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
            return {'user': {k: v if type(v) not in [date, datetime] else v.strftime('%Y-%m-%d') for k, v in vars(user).items()}, 'status_code': 200}
        except DBError:
            return {'msg': 'Duplication Error', 'status_code': 400}
    except Exception as e:
        return {'msg': 'Server Error', 'status_code': 500}


@login_required
def show_profile(request):
    data = {k: v if type(v) not in [datetime, date] else v.strftime('%Y-%m-%d') for (k, v) in
            vars(request.session.user).items()}
    data['status_code']: 200
    return data
