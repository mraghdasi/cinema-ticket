import json

from src.client.auth import register
from src.server.models.user import User

request_data = json.loads(register.main())
user = User.objects.create(**request_data['payload'])
User.objects.update({'role': 0}, f'id={user.id}')
print("Admin Successfully Created")
