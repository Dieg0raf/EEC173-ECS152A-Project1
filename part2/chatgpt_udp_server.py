import socket
import time

# Server settings
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 4096  # Size of each data packet received (in bytes)

# Create a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    # Bind the socket to the server address and port
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    print(f"Server listening on {SERVER_ADDRESS}:{SERVER_PORT}")

    # Receive data from the client
    total_data_received = 0  # Total bytes received
    start_time = time.time()  # Start time for throughput measurement

    while True:
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        total_data_received += len(data)

        # Check for termination message from client
        if data == b'DONE':
            break

    end_time = time.time()  # End time for throughput measurement

    # Calculate throughput in kilobytes per second (KBps)
    total_kb_received = total_data_received / 1024
    elapsed_time = end_time - start_time
    throughput = total_kb_received / elapsed_time if elapsed_time > 0 else 0

    # Send throughput result back to client
    server_socket.sendto(str(throughput).encode(), client_address)
    print(f"Total data received: {total_kb_received:.2f} KB, Time: {elapsed_time:.2f}s, Throughput: {throughput:.2f} KBps")
