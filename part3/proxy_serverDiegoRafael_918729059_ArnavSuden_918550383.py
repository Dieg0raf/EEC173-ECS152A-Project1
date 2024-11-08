import socket
import json
from concurrent.futures import ThreadPoolExecutor

# specify host and port to listen on
HOST = '127.0.0.1'
PORT = 65430

# Random list of IP addresses to block
IP_BLOCK_LIST = {
    "127.2.1.0" : True,
    "172.16.0.1": True,
    "192.168.100.100": True,
    "10.10.10.10": True,
}

# function to run in separate thread and handle client
def handle_client(client_socket, client_addr, client_port):

    with client_socket:
        # Allows for persistent connection with client
        while True:
            # receive data from client
            data = client_socket.recv(1024)
            if not data:
                client_socket.close()
                break

            # parse data
            received_data = json.loads(data.decode('utf-8'))
            server_address = received_data["server_ip"]
            server_port = received_data["server_port"]

            # Check if destination server is on the block list
            if server_address in IP_BLOCK_LIST:
                client_socket.sendall((f"Error: {server_address} is Blocked").encode("utf-8"))
                client_socket.close()

            # establish/connect new proxy server tcp connection to destination server (non-persistent connection with server)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.connect((server_address, server_port))
                print(f"Connected to server")

                # sending client request to server
                server_socket.sendall(received_data["message"].encode("utf-8"))

                # send server response to client
                received_message = server_socket.recv(1024)
                if received_message:
                    client_socket.sendall(received_message)
                    print("Forwarded response to client")
                else:
                    client_socket.sendall(b"Server doesn't have a response")

# Create TCP listening socket for proxy server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:

    # set proxy socket and listening mode
    proxy_socket.bind((HOST, PORT))
    proxy_socket.listen()

    # Allow for multiple clients to connect at the same time
    with ThreadPoolExecutor(max_workers=3) as executor:
        while True:
            # accept a new connection
            client_socket, (client_addr, client_port) = proxy_socket.accept()

            # spawn new parallel thread for new client
            executor.submit(handle_client, client_socket, client_addr, client_port)