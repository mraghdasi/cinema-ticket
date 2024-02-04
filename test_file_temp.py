from src.server.models.hall import Hall
from src.server.models.user import User

# operations = DBOperation()

user1 = User.objects.create('soroush123', 'sorm1379@gmail.com', '09390468833', 'pAssWd120@#!', '1379-12-16')
hall1 = Hall.objects.create('title1', 30)
print(vars(user1))
print(vars(hall1))


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