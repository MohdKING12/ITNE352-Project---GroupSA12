import socket
import threading
import json
from api import *

HOST = 'localhost'
PORT = 5000

clients = []
flight_data = []

def handle_client(conn, addr):
    global flight_data
    print(f"[+] New connection from {addr}")
    
    # Receive username
    username = conn.recv(1024).decode()
    print(f"[*] Client identified as {username}")

    while True:
        try:
            request = conn.recv(1024).decode()
            if not request or request.lower() == 'quit':
                break

            print(f"[>] Received request from {username}: {request}")

            if request == "arrived":
                response_data = get_arrived_flights(flight_data)
            elif request == "delayed":
                response_data = get_delayed_flights(flight_data)
            elif request.startswith("details "):
                code = request.split(" ")[1]
                response_data = get_flight_details(code)
            else:
                response_data = "Invalid request"

            response_str = json.dumps(response_data, indent=2)
            conn.sendall(response_str.encode())

        except Exception as e:
            print(f"[!] Error with client {username}: {e}")
            break

    conn.close()
    print(f"[-] Connection with {username} closed")


def start_server():
    
    global flight_data
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}")

    # Get airport code and fetch flight data once at startup
    airport_code = input("Enter ICAO code of the airport: ")
    flight_data = fetch_flights_by_airport(airport_code)

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        clients.append(conn)
        print(f"[#] Active connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
