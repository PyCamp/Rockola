
import requests


URL = 'http://localhost:5000/vote'

data = {'track_id': 10, 'operation': 'votopositivo'}

r = requests.get(URL, params=data)
