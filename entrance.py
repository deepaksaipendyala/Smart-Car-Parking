import socket

# Server configuration
HOST = '172.20.10.2'  # Server IP address
PORT = 49000  # Server port

# Create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Connected to client: {client_address}")

# Receive and process data from the client
while True:
    data = client_socket.recv(1024).decode()
    if not data:
        break
    sensor_data = data.split(",")
    if len(sensor_data) == 2:
        ir_1_status, ir_2_status = sensor_data
        print("IR Sensor 1 status:", ir_1_status)
        print("IR Sensor 2 status:", ir_2_status)

# Close the client connection
client_socket.close()

# Close the server socket
server_socket.close()
