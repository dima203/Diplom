import requests
from requests.auth import HTTPBasicAuth


request = requests.get('http://127.0.0.1:8000/api/users/', auth=HTTPBasicAuth('admin', 'admin'))
print(request.json())
