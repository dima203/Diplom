import requests


token = requests.post('http://127.0.0.1:8000/api/token/', data={'username': 'admin', 'password': 'admin'}).json()['access']
request = requests.get('http://127.0.0.1:8000/api/resource_types/', headers={'Authorization': f'Bearer {token}'})
print(request.json())
