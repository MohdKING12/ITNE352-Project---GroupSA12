import requests
import json

API_KEY = '626b50b0a1b2662767b3c78113182944'  
BASE_URL = 'https://api.aviationstack.com/v1/flights'

# Save fetched data to JSON
def save_to_file(data, filename='group_SA12.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Fetch flight data for an airport
def fetch_flights_by_airport(icao_code):
   
    params = {
        'access_key': API_KEY,
        'arr_icao': icao_code,
        'limit': 100
    }

    response = requests.get(BASE_URL, params=params)
   
    if response.status_code == 200:
        data = response.json().get('data', [])
        save_to_file(data)
        return data
   
    else:
   
        print("Error:", response.status_code)
        return []

# Get arrived flights
def get_arrived_flights(data):
    
    arrived = []
    for flight in data:
        if flight.get('flight_status') == 'landed':
            arrived.append(flight)

    results = []
   
    for flight in arrived:
   
        results.append({
            'Flight Code': flight['flight']['iata'],
            'Departure Airport': flight['departure']['airport'],
            'Arrival Time': flight['arrival']['actual'],
            'Arrival Terminal': flight['arrival']['terminal'],
            'Arrival Gate': flight['arrival']['gate']
        })
   
    return results

# Get delayed flights
def get_delayed_flights(data):
    
    delayed = []
    for flight in data:
   
        delay = flight.get('departure', {}).get('delay')
        results = []

        if delay and delay > 0: # if delay is not none or null & it is > 0
   
            results.append({
                'Flight Code': flight['flight']['iata'],
                'Departure Airport': flight['departure']['airport'],
                'Scheduled Departure': flight['departure']['scheduled'],
                'Estimated Arrival': flight['arrival']['estimated'],
                'Delay (min)': flight['arrival']['delay'],
                'Arrival Terminal': flight['arrival']['terminal'],
                'Arrival Gate': flight['arrival']['gate']
            })
   
    return results

# Get details of a specific flight
def get_flight_details(iata_code):
   
    params = {
        'access_key': API_KEY,
        'flight_iata': iata_code
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        
        if not data:
            return 'There are no data for this flight, try another flight!'
        
        flight = data[0]

        return {
            'Flight Code': flight['flight']['iata'],
            'Departure Airport': flight['departure']['airport'],
            'Departure Terminal': flight['departure']['terminal'],
            'Departure Gate': flight['departure']['gate'],
            'Arrival Airport': flight['arrival']['airport'],
            'Arrival Terminal': flight['arrival']['terminal'],
            'Arrival Gate': flight['arrival']['gate'],
            'Status': flight['flight_status'],
            'Scheduled Departure': flight['departure']['scheduled'],
            'Scheduled Arrival': flight['arrival']['scheduled']
        }
    else:
        print("Error:", response.status_code)
        return None