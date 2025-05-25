import socket
import json

HOST = '127.0.0.1'
PORT = 65432

def connect_to_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        return s
    except Exception as e:
        print(f"Connection error: {e}")
        return None



def send_username(sock, name):
    try:
        sock.sendall(name.encode())
    except Exception as e:
        print(f"Error sending username: {e}")



def send_request(sock, request):

    try:
        sock.sendall(request.encode())
        if request.lower() == 'quit':
            return
        
        else:
            
            all_received = b""
            while True:
                try:
                    data = sock.recv(4096)
                    all_received += data
                    if len(data) < 4096:
                        break
                except Exception as e:
                    print(f"Error receiving data: {e}")
                    return None
            
            try:
                data_to_send = json.loads(all_received.decode("utf-8"))      
                return data_to_send
            
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                return data_to_send.decode("utf-8")  # Return as string if not JSON
            
            except Exception as e:
                print(f"Error processing response: {e}")
                return None
    
    except Exception as e:
        print(f"Error sending request: {e}")
        return None