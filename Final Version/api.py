import requests
import json

API_KEY = 'b36b8c12877478dc53575afb98e74398'  
BASE_URL = 'https://api.aviationstack.com/v1/flights'

# Save fetched data to JSON
def save_to_file(data, filename='group_SA12.json'):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except json.JSONEncodeError as e:
        print(f"JSON encoding error: {e}")
    except Exception as e:
        print(f"File write error: {e}")

# Fetch flight data for an airport
def get_flights_by_airport_code(icao_code): 
    params = {
        'access_key': API_KEY,
        'arr_icao': icao_code,
        'limit': 100
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
       
        if response.status_code == 200:
            try:
                data = response.json().get('data',[])
                
                if not data:
                    print("There is no information for this airport")
                    return data
                
                else:
                    save_to_file(data)
                    return data
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                return []
       
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
        
    except requests.exceptions.RequestException as e:
        print(f"API connection error: {e}")
        return []
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []




# Get arrived flights from JSON file
def get_arrived_flights(data=None):

    try:
        # Read from JSON file
        with open('group_SA12.json', 'r') as f:
            data = json.load(f)

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return []

    except Exception as e:
        print(f"File read error: {e}")
        return []
    
    arrived = []
    for flight in data:
        if flight.get('flight_status') == 'landed':
            arrived.append(flight)

    results = []
   
    for flight in arrived:
        flight_info = {
            'Flight Code': flight['flight'].get('iata', 'N/A'),
            'Departure Airport': flight['departure'].get('airport', 'N/A'),
            'Arrival Time': flight['arrival'].get('actual', 'N/A'),
            'Arrival Terminal': flight['arrival'].get('terminal', 'N/A'),
            'Arrival Gate': flight['arrival'].get('gate', 'N/A')
        }

        results.append(flight_info)
   
    return results



# Get delayed flights from JSON file
def get_delayed_flights(data=None):

    try:
        # Read from JSON file
        with open('group_SA12.json', 'r') as f:
            data = json.load(f)

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return []

    except Exception as e:
        print(f"File read error: {e}")
        return []
    
    results = []
    
    for flight in data:
        delay = flight.get('departure', {}).get('delay')
        if delay and delay > 0:        # if delay exist and is more than 0
            flight_info = {
                'Flight Code': flight['flight'].get('iata', 'N/A'),
                'Departure Airport': flight['departure'].get('airport', 'N/A'),
                'Scheduled Departure': flight['departure'].get('scheduled', 'N/A'),
                'Estimated Arrival': flight['arrival'].get('estimated', 'N/A'),
                'Delay (min)': flight['departure'].get('delay', 'N/A'),
                'Arrival Terminal': flight['arrival'].get('terminal', 'N/A'),
                'Arrival Gate': flight['arrival'].get('gate', 'N/A')
            }
            results.append(flight_info)
   
    return results




# Get details of a specific flight
def get_flight_details(iata_code):
    params = {
        'access_key': API_KEY,
        'flight_iata': iata_code
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json().get('data', [])
                
                if not data:
                    return 'There are no data for this flight, try another flight!'
                
                flight = data[0]

                return {
                    'Flight Code': flight['flight'].get('iata', 'N/A'),
                    'Departure Airport': flight['departure'].get('airport', 'N/A'),
                    'Departure Terminal': flight['departure'].get('terminal', 'N/A'),
                    'Departure Gate': flight['departure'].get('gate', 'N/A'),
                    'Arrival Airport': flight['arrival'].get('airport', 'N/A'),
                    'Arrival Terminal': flight['arrival'].get('terminal', 'N/A'),
                    'Arrival Gate': flight['arrival'].get('gate', 'N/A'),
                    'Status': flight.get('flight_status', 'N/A'),
                    'Scheduled Departure': flight['departure'].get('scheduled', 'N/A'),
                    'Scheduled Arrival': flight['arrival'].get('scheduled', 'N/A')
                }
            except json.JSONDecodeError as e:
                return f"JSON decode error: {e}"
      
        else:
            return f"Error fetching flight details: {response.status_code}"
    
    except requests.exceptions.RequestException as e:
        return f"API connection error: {e}"
    
    except Exception as e:
        return f"Unexpected error: {e}"