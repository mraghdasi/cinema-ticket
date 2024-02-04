from src.server.models.cinema_sans import CinemaSans

# operations = DBOperation()

# user1 = User.objects.create('soroush12321233', 'sorm1379@gmail.com', '09390468833', 'pAssWd120@#!', '1379-12-16')
# hall1 = Hall.objects.create('title1', 30)
# user1 = User.objects.read('username="soroush12321233"')
# user1 = user1[0]
# print(user1)
# user1.set_user_logged_out()
# user1 = User.objects.read(f'id={user1.id}')
# user1 = user1[0]
# print(user1.is_logged_in)

# for user in User.objects.read():
#     print(user.id)
#
# for hall in Hall.objects.read():
#     print(hall.id)

# users = User.objects.update({'phone_number': '09390468833'})
# print(vars(users[0]))

# for i in range(5):
#     User.objects.create(f'soroush123{i}', f'sorm1379{i}@gmail.com', f'09390468{i}83', 'pAssWd120@#!', '1379-12-16')

# User.objects.delete('Role = 1')
#
# for user in User.objects.read():
#     print(user)

# import time
# user1 = User.objects.read('id=56')[0]
# package1 = Package.objects.create('Gold', 50, 50000)
# subs1 = Subscription.objects.create(user1.id, package1.id, time.strftime('%Y-%m-%d %H:%M:%S'))
# print(subs1.user_id)
from src.server.models.film import Film
from src.server.models.hall import Hall

film1 = Film.objects.create('Film2', 20)
hall1 = Hall.objects.create('Hall2', 100)
CinemaSans.objects.create('12:12:00', '14:00:00', film1.id, hall1.id, 5000)
CinemaSans.objects.create('12:12:00', '14:00:00', film1.id, hall1.id, 5000)
CinemaSans.objects.create('12:12:00', '14:00:00', film1.id, hall1.id, 5000)
CinemaSans.objects.create('12:12:00', '16:00:00', film1.id, hall1.id, 4000)
CinemaSans.objects.create('12:12:00', '14:00:00', film1.id, hall1.id, 5000)
CinemaSans.objects.create('12:12:00', '14:00:00', film1.id, hall1.id, 5000)
CinemaSans.objects.create('16:12:00', '18:00:00', film1.id, hall1.id, 1000)
CinemaSans.objects.create('12:12:00', '14:00:00', film1.id, hall1.id, 5000)
CinemaSans.objects.create('12:12:00', '14:00:00', film1.id, hall1.id, 5000)
q = """
select *
from cinema_sans
join cinema_ticket.film film on cinema_sans.film_id = film.id
join cinema_ticket.hall hall on hall.id  = cinema_sans.hall_id
"""
list1 = CinemaSans.objects.query(q, fetch=True)
print(list(map(vars, list1)))
