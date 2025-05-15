import socket
import json

HOST = '127.0.0.1'  # IP address of the server
PORT = 65432        # Must match the server port

def receive_response(sock):
    try:
        data = sock.recv(4096).decode()
        try:
            parsed = json.loads(data)
            if isinstance(parsed, list):
                for flight in parsed:
                    print("\n--- Flight ---")
                    for k, v in flight.items():
                        print(f"{k}: {v}")
            elif isinstance(parsed, dict):
                print("\n--- Flight Details ---")
                for k, v in parsed.items():
                    print(f"{k}: {v}")
            else:
                print(parsed)
        except json.JSONDecodeError:
            print(data)
    except Exception as e:
        print("Error receiving response:", e)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print("Cannot connect to server. Make sure it is running.")
            return

        username = input("Enter your name: ")
        s.sendall(username.encode())

        while True:
            print("\n--- Flight Information Menu ---")
            print("1. View Arrived Flights")
            print("2. View Delayed Flights")
            print("3. View Particular Flight Details")
            print("4. Quit")

            choice = input("Enter option (1-4): ").strip()

            if choice == '1':
                s.sendall("1".encode())
                receive_response(s)

            elif choice == '2':
                s.sendall("2".encode())
                receive_response(s)

            elif choice == '3':
                code = input("Enter Flight IATA Code (e.g., GF003): ").strip().upper()
                s.sendall(f"3:{code}".encode())
                receive_response(s)

            elif choice == '4':
                s.sendall("quit".encode())
                print("Disconnected from server.")
                break

            else:
                print("Invalid option. Please try again.")

