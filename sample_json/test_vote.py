
import requests


URL = 'http://localhost:5000/vote'

data = {'track_id': 10, 'operation': 'positivo'}

r = requests.get(URL, params=data)
