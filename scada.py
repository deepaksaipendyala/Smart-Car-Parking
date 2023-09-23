import sqlite3
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

# Create a database connection
conn = sqlite3.connect('parking.db')
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS parking (
                car_slot TEXT,
                time TEXT,
                available_slots TEXT
            )''')

# Function to insert data into the database
def insert_data(car_slot, available_slots):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO parking VALUES (?, ?, ?)", (car_slot, time, available_slots))
    conn.commit()

# Function to retrieve data from the database
def retrieve_data():
    c.execute("SELECT * FROM parking")
    data = c.fetchall()
    return data

# Function to refresh the GUI
def refresh_gui():
    data = retrieve_data()
    text.delete('1.0', tk.END)  # Clear the text widget
    for row in data:
        text.insert(tk.END, f"Car Slot: {row[0]}\n")
        text.insert(tk.END, f"Time: {row[1]}\n")
        text.insert(tk.END, f"Available Slots: {row[2]}\n\n")

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
                        if data_from_client_1:
                            # Send the data to client 2
                            print("Sending data to client:", data_from_client_1)
                            client_socket.sendall(bytes(data_from_client_1))
                            insert_data("4", "[1,2,3]")
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
window = tk.Tk()
window.title("Parking System")

label = tk.Label(window, text="Parking Information", font=("Helvetica", 16))
label.pack(pady=10)

text = tk.Text(window, width=40, height=10)
text.pack(pady=10)

refresh_button = tk.Button(window, text="Refresh", command=refresh_gui)
refresh_button.pack(pady=10)

# # Insert some sample data
# insert_data("1", "[1,2,3]")
# insert_data("2", "[1,2,3]")
# insert_data("3", "[1,2,3]")

# Refresh the GUI initially
refresh_gui()

# Start the main GUI loop
window.mainloop()

# Close the database connection
conn.close()
