import machine
import utime
import socket           # Import socket module

# Create a socket object
s = socket.socket()     

# IP address and port to listen on
HOST = "192.168.191.90"
PORT = 50000

# connect to the server on local computer
s.connect((HOST,PORT))

# receive data from the server and decoding to get the string.
#data=s.recv(1024)

#print ("message from server:",data)
 
# s.sendall(b"This is a hello from client Raspi")
    

ir1 = machine.Pin(0, machine.Pin.IN)
ir2 = machine.Pin(1, machine.Pin.IN)
ir4 = machine.Pin(2, machine.Pin.IN)
ir3 = machine.Pin(3, machine.Pin.IN)

led = machine.Pin('LED', machine.Pin.OUT)

while True:
    slots = []
    if ir1.value() == 1:
        print("Slot 1 Free!")
        slots.append(1)
    if ir2.value() == 1:
        print("Slot 2 Free!")
        slots.append(2)
    if ir3.value() == 1:
        print("Slot 3 Free!")
        slots.append(3)
    if ir4.value() == 1:
        
        print("Slot 4 Free!")
        slots.append(4)
        
    if len(slots) != 0:
        print(slots)
        s.sendall(bytes(slots))
    else:
        print('no slots')
        s.sendall(b'no')

    utime.sleep(5)
    # Send information of empty slots to SCADA master through connection 1
    # connection_1.send(empty_slots) # Uncomment this line and replace `connection_1` with the name of your connection object

s.sendall(b"Connection closing")

# close the connection
s.close() 