import utime
import random
from servo import Servo
import socket           # Import socket module
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd

# Create a socket object
s = socket.socket()     

# IP address and port to listen on
HOST = "192.168.191.90"
PORT = 50000

# connect to the server on local computer
s.connect((HOST,PORT))
s.sendall(b'HI')
# receive data from the server and decoding to get the string.
    

s1 = Servo(0)       # Servo pin is connected to GP0

ir = machine.Pin(1, machine.Pin.IN)

led = machine.Pin('LED', machine.Pin.OUT)

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
 
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s1.goto(round(servo_Map(angle,0,180,0,1024))) # Convert range value to angle value

def open_gate():
    print("Opening gate...")
    servo_Angle(90)
    utime.sleep(1)

def close_gate():
    print("Closing gate...")
    servo_Angle(0)
    utime.sleep(1)

if __name__ == '__main__':
     c = 0
     while True:
         if ir.value() == 0 and c==0:
                 c=1
                 lis=s.recv(1024)
                 lis = list(map(lambda x: int(x), lis))
                 print("Slots ",lis)
                 if lis[0]==110 and lis[1]==111:
                     lcd.move_to(0,0)
                     txt = "No Slots"
                     lcd.putstr(str(txt))
                 else:
                     lcd.move_to(0,0)
                     txt = "slot"+str(lis[0])
                     lcd.putstr(str(txt))
                     lcd.move_to(0,1)
                     lcd.putstr(str(lis))
#                  lcd.move_to(0,0)
#                  txt = "slot"+str(lis[0])
#                  lcd.putstr(str(txt))
#                  lcd.move_to(0,1)
#                  lcd.putstr(str(lis))                
                 s.sendall(bytes(txt,lis[0]))
                 led.value(1)
                 print("IR Sensor Detected!")
                 led.value(0)
                 open_gate()
                 c=1  
         elif ir.value()==1 and c==1:
             c = 0
             close_gate()
            
     s.sendall(b"Connection closing")

     # close the connection
     s.close()