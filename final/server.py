import socket
import threading
import logging
from datetime import datetime
import tkinter as tk

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Server details
server_ip = '192.168.191.90'  # Server IP address
server_port = 50000

# Create a lock for thread synchronization
lock = threading.Lock()

# Dictionary to store client data
client_data = {}

# File to store data
data_file = "data.txt"

# Function to save data to a file
def save_data(data):
    with open(data_file, "a") as file:
        file.write(data + "\n")

# Function to retrieve data from the file
def retrieve_data():
    with open(data_file, "r") as file:
        data = file.readlines()
    return data

# Function to refresh the GUI
def refresh_gui():
    data = retrieve_data()
    text.delete('1.0', tk.END)  # Clear the text widget
    for line in data:
        text.insert(tk.END, line)

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
                        data1 = list(map(lambda x: int(x), data))
                        client_data[client_address[0]] = data1
                        print("Message from client:", data1)
                        # Save data to file
                        save_data(f"{client_address[0]}: {data1}")
                        print("Data saved to file")

                elif client_address[0] == '192.168.191.3':
                    with lock:
                        data_from_client_1 = client_data.get('192.168.191.200')
                        if data_from_client_1:
                            # Send the data to client 2
                            print("Sending data to client:", data_from_client_1)
                            client_socket.sendall(bytes(data_from_client_1))
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

# Function to start the server
def start_server():
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

        # Create a thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# GUI setup
# GUI setup
window = tk.Tk()
window.title("Parking System")

label = tk.Label(window, text="Parking Information", font=("Helvetica", 16))
label.pack(pady=10)

text = tk.Text(window, width=40, height=10)
text.pack(pady=10)

refresh_button = tk.Button(window, text="Refresh", command=refresh_gui)
refresh_button.pack(pady=10)

# Refresh the GUI initially
refresh_gui()

# Start the main GUI loop
window.mainloop()

