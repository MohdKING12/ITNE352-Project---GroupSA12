import socket
import json

HOST = '127.0.0.1'
PORT = 65432

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def send_username(sock, name):
    sock.sendall(name.encode())

def send_request(sock, request):
    sock.sendall(request.encode())
    while True:
        data = sock.recv(1024).decode()
        if not data:
            break
    
    try:
        return json.loads(data)
    
    except json.JSONDecodeError:
        return data
