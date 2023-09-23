import socket
import threading
import logging

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Server details
server_ip = '192.168.191.90'  # Server IP address
server_port = 50000

# Create a lock for thread synchronization
lock = threading.Lock()

# Dictionary to store client data
client_data = {}

# Function to handle client connections
def handle_client(client_socket, client_address):
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if data:
                if client_address[0] == '192.168.191.200':
                    with lock:
                        # Store the received data in the client_data dictionary
                        data = list(map(lambda x: int(x), data))
                        client_data[client_address[0]] = data
                        print("Message from client:", data)

                elif client_address[0] == '192.168.191.3':
                    with lock:
                        data_from_client_1 = client_data.get('192.168.191.200')
                        slot = data_from_client_1[0]
                        if data_from_client_1:
                            # Send the data to client 2
                            print("Sending data to client:", data_from_client_1)
                            client_socket.sendall(bytes(data_from_client_1))
                            print("Slot:",slot)
    except Exception as e:
        logging.error(f'Error handling client {client_address[0]}: {str(e)}')

    finally:
        with lock:
            # Remove the client data from the dictionary when the client disconnects
            if client_address[0] in client_data:
                del client_data[client_address[0]]

        # Close the client socket
        client_socket.close()

# Create a socket object
server_socket = socket.socket()

# Bind the socket to a specific IP address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen()
print(f'Server listening on {server_ip}:{server_port}')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,client_address))
    # print(client_socket,client_address)
    client_thread.start()
