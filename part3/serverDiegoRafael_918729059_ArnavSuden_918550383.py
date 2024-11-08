import socket
import json
from concurrent.futures import ThreadPoolExecutor

# specify host and port to listen on
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65420

# function to run in separate thread and handle client
def handle_client(client_socket, client_addr, client_port):

    # non-persistent connection with client
    with client_socket:

        # receive data from client
        data = client_socket.recv(1024)
        if not data:
            client_socket.close()
        
        # generate response back to it's client
        if data == b"ping":
            print(f"Received {data.decode()!r} from {client_addr}:{client_port}")
            client_socket.sendall(b'pong')
        else:
            client_socket.sendall((f"404 Not Found - Couldn't find {data.decode()!r}").encode("utf-8"))

# creates new TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    # set listening mode on for this socket
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()

    # thread pool to contain all threads
    with ThreadPoolExecutor(max_workers=3) as executor:

        # run indefinitely
        while True:
            # accept a new connection
            client_socket, (client_addr, client_port) = server_socket.accept()
            print(f"Connected to {client_addr}:{client_port}")

            # spawn new parallel thread for new client
            # main thread will continue back to accept new clients
            executor.submit(handle_client, client_socket, client_addr, client_port)