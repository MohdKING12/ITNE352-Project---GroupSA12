import requests
import json
import api 

API_KEY = '626b50b0a1b2662767b3c78113182944'  
BASE_URL = 'https://api.aviationstack.com/v1/flights'
data = ''
def save_to_file(data, filename='group_SA12.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


params = {
        'access_key': API_KEY,
        'arr_icao': 'UWUU',
        'limit': 100
    }
    
response = requests.get(BASE_URL, params=params)
if response.status_code == 200:
    data = response.json().get('data', [])
    save_to_file(data)



arrive= api.get_arrived_flights(data)
delay= api.get_delayed_flights(data)

print('\n',delay)