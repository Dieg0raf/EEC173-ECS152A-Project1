import socket

# specify server host and port to connect to
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5500

# open a new datagram socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:

    # construct message of 4096 Bytes
    message = b" " * 4096
    size_of_message = len(message)
    amount_of_data_sent = 0

    print("---- Throughput test starting ----")

    # send message of size 4096 Bytes to server until client sends 10MB
    while True:

        # send message to server
        client_socket.sendto(message, (SERVER_HOST, SERVER_PORT))
        amount_of_data_sent += size_of_message

        # check if client sent 100 MB
        if amount_of_data_sent >= (100 * 1024 * 1024):

            # send last message telling server test it completed
            final_message = b"Completed Test"
            client_socket.sendto(final_message, (SERVER_HOST, SERVER_PORT))

            # receive response and check if it's the last response from the server
            message_received = client_socket.recv(1024)
            if (message_received[0:10] == b'Calculated'):
                print(f"Total Data sent: {(amount_of_data_sent /1024) / 1024} MB")
                print(message_received.decode())
                print("---- Throughput test ending ----")

            break