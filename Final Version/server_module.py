import socket
import threading
import json
from api import get_flights_by_airport_code, get_arrived_flights, get_delayed_flights, get_flight_details

no_data = "There is no information for this airport"
HOST = '127.0.0.1'
PORT = 65432
clients = {}

def handle_client(conn, addr, all_flights):
    try:
        name = conn.recv(1024).decode()
        clients[addr] = name
        print(f"[NEW CONNECTION] {name} connected from {addr}\n")

        while True:
            try:
                data = conn.recv(1024).decode()
                
                if not data or data.lower() == 'quit':
                    print(f"[DISCONNECT] {name} has disconnected.")
                    break
                
                print(f"[REQUEST] From {name}: {data}")
                
                if data == '1':
                    results = get_arrived_flights(all_flights)
                    try:
                        conn.sendall(json.dumps(results).encode("ascii"))
                    except json.JSONEncodeError as e:
                        print(f"[JSON ERROR] Failed to encode arrived flights: {e}")
                        conn.sendall("Error: Failed to process arrived flights data".encode())

                elif data == '2':
                    results = get_delayed_flights(all_flights)
                    try:
                        conn.sendall(json.dumps(results).encode())
                    except json.JSONEncodeError as e:
                        print(f"[JSON ERROR] Failed to encode delayed flights: {e}")
                        conn.sendall("Error: Failed to process delayed flights data".encode())

                elif data.startswith('3:'):
                    flight_code = data.split(":")[1].strip()
                    details = get_flight_details(flight_code)
                    try:
                        conn.sendall(json.dumps(details).encode())
                    except json.JSONEncodeError as e:
                        print(f"[JSON ERROR] Failed to encode flight details: {e}")
                        conn.sendall("Error: Failed to process flight details".encode())

                else:
                    conn.sendall("Invalid option.".encode())
                    
            except ConnectionResetError:
                print(f"[CONNECTION ERROR] {name} connection reset by peer")
                break
            except Exception as e:
                print(f"[ERROR] Error handling request from {name}: {e}")
                try:
                    conn.sendall("Server error occurred".encode())
                except:
                    break

    except Exception as e:
        print(f"[ERROR] Error in client handler for {addr}: {e}")
    finally:
        try:
            conn.close()
            if addr in clients:
                del clients[addr]
        except Exception as e:
            print(f"[CLEANUP ERROR] {e}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print('[SERVER] Listening...')

        while True:
            try:
                conn, addr = server.accept()
                
                try:
                    icao = conn.recv(1024).decode()
                    all_flights = get_flights_by_airport_code(icao)
                   
                    # Handle case when no flights are found
                    if not all_flights:
                        print(f"[INFO] No flight data for {icao}.")
                        try:
                            conn.sendall(no_data.encode())
                        except Exception as e:
                            print(f"[SEND ERROR] {e}")
                        finally:
                            conn.close()
                        continue
                    
                    print(f"[INFO] Flights fetched for {icao}.\nWaiting for requests...")

                    thread = threading.Thread(target=handle_client, args=(conn, addr, all_flights))
                    thread.daemon = True
                    thread.start()
                    print(f"\n[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
                    
                except Exception as e:
                    print(f"[CONNECTION SETUP ERROR] {e}")
                    try:
                        conn.close()
                    except:
                        pass
                        
            except Exception as e:
                print(f"[ACCEPT ERROR] {e}")
                
    except Exception as e:
        print(f"[SERVER ERROR] {e}")
    finally:
        try:
            server.close()
        except:
            pass

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
    except Exception as e:
        print(f"[MAIN ERROR] {e}")