import socket

# Client settings
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 4096  # Size of each data packet sent (in bytes)
TOTAL_DATA_SIZE = 100 * 1024 * 1024  # 100 MB in bytes

# Create a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    # Send 100 MB of data in chunks
    total_data_sent = 0
    data_chunk = b'a' * BUFFER_SIZE  # Sample data packet

    while total_data_sent < TOTAL_DATA_SIZE:
        client_socket.sendto(data_chunk, (SERVER_ADDRESS, SERVER_PORT))
        total_data_sent += BUFFER_SIZE

    # Send termination message to notify the server all data is sent
    client_socket.sendto(b'DONE', (SERVER_ADDRESS, SERVER_PORT))

    # Receive throughput result from the server
    throughput_data, _ = client_socket.recvfrom(BUFFER_SIZE)
    throughput = float(throughput_data.decode())
    print(f"Throughput received from server: {throughput:.2f} KBps")
