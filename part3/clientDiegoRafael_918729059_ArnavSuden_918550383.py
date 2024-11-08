import socket
import json
from time import sleep

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 65430

# creates new TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    # Establishing connection to proxy server
    client_socket.connect((PROXY_HOST, PROXY_PORT))
    print("Connected to proxy server")

    while True:
        # Send data to proxy server
        data = {
            "server_ip": "127.0.0.1",
            "server_port": 65420,
            "message": "ping"
        }

        # Send data to proxy server (json string) - serialize data to json string
        serialized_data = json.dumps(data).encode('utf-8')
        client_socket.sendall(serialized_data)

        # Receive data from proxy server
        received_message = client_socket.recv(1024)
        print(f"Received {received_message.decode()!r} from {PROXY_HOST}:{PROXY_PORT}")
        sleep(1)