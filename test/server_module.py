import socket
import threading
import json
from api import get_flights_by_airport_code, get_arrived_flights, get_delayed_flights, get_flight_details

no_data="There is no information for this airport"
HOST = '127.0.0.1'
PORT = 65432
clients = {}

def handle_client(conn, addr, all_flights):
   
    try:
        name = conn.recv(1024).decode()
        clients[addr] = name
        print(f"[NEW CONNECTION] {name} connected from {addr}")

        while True:

            data = conn.recv(1024).decode()
            if not data or data.lower() == 'quit':
                print(f"[DISCONNECT] {name} has disconnected.")
                break

            print(f"[REQUEST] From {name}: {data}")

            if data == '1':
                results = get_arrived_flights(all_flights)
                conn.sendall(json.dumps(results).encode())

            elif data == '2':
                results = get_delayed_flights(all_flights)
                conn.sendall(json.dumps(results).encode())

            elif data.startswith('3:'):
                flight_code = data.split(":")[1].strip()
                details = get_flight_details(flight_code)
                conn.sendall(json.dumps(details).encode())

            else:
                conn.sendall("Invalid option.".encode())

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        del clients[addr]

def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print('[SERVER] Listening...')

    while True:
        conn, addr = server.accept()
        icao = conn.recv(1024).decode()
        all_flights = get_flights_by_airport_code(icao)
       
        if all_flights.lower()==no_data.lower():
           print(all_flights)
           continue
        
        print(f"[INFO] Flights fetched for {icao}.\n Waiting for requests...")

        thread = threading.Thread(target=handle_client, args=(conn, addr, all_flights))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
