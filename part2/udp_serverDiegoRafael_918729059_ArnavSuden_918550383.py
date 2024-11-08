import socket
import time

# specify host and port to receive messages on
HOST = '127.0.0.1'
PORT = 5500


# create a new datagram socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:

    # bind this socket to OS
    server_socket.bind((HOST, PORT))
    print("iPerf server running...\n")

    # variable declarations
    amount_of_data_received = 0
    prev_client_info = None
    start_time = 0
    end_time = 0
    count = 0

    while True:
            # receive requests from clients
            data, client_info = server_socket.recvfrom(4096)

            # keep track of new client
            if client_info != prev_client_info:
                start_time = time.time()
                amount_of_data_received = 0
                prev_client_info = client_info
                count = count + 1

                print(f"---Server Starting Test {count}---")
                print(f"local {HOST} port {PORT} connected to {client_info[0]} port {client_info[1]}")
            
            # updates bytes received from current client
            if data and client_info == prev_client_info:
                amount_of_data_received += len(data)

            # client sent 100MB (packets could've been lost) - throughput calculations
            if data == b'Completed Test':
                end_time = time.time()
                final_time = end_time - start_time
                throughput = (amount_of_data_received / (1024)) / final_time

                # send final response to client
                final_message = f"Calculated throughput: {throughput:.2f} KB/s".encode()
                server_socket.sendto(final_message, client_info)
                print(f"Total Data received: {((amount_of_data_received /1024) / 1024):.2f}MB\nTime Taken: {final_time:.2f} seconds\nCalculated throughput: {throughput:.2f} KB/s")
                print(f"---Server Finishing Test {count}---\n")

    print("iPerf server stopping...")