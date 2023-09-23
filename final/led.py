import time
import random
from machine import UART

# Modbus RTU Configuration
RTU_PORT = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=0, rx=1)  # UART port connected to the SCADA master
RTU_ADDRESS = 1                                                            # RTU address (1 to 247)

# Sensor Pins (Modify according to your setup)
SENSOR_PIN_1 = 2
SENSOR_PIN_2 = 3

# Actuator Pins (Modify according to your setup)
ACTUATOR_PIN_1 = 4
ACTUATOR_PIN_2 = 5

# Function to read data from sensors
def read_sensors():
    sensor1_value = random.randint(0, 100)  # Simulating sensor data
    sensor2_value = random.randint(0, 100)  # Simulating sensor data
    return sensor1_value, sensor2_value

# Function to control actuators
def control_actuators(actuator1_value, actuator2_value):
    # Implement your actuator control logic here
    # For example, you can use GPIO library to set actuator pins high/low
    pass

# Main loop
while True:
    try:
        # Read sensor values
        sensor1, sensor2 = read_sensors()
        
        # Send sensor data to the SCADA master
        RTU_PORT.write([RTU_ADDRESS, 6, 0, 0, sensor1 >> 8, sensor1 & 0xFF])  # Assuming register address 0 for sensor1
        RTU_PORT.write([RTU_ADDRESS, 6, 0, 1, sensor2 >> 8, sensor2 & 0xFF])  # Assuming register address 1 for sensor2
        
        # Read actuator values from the SCADA master
        RTU_PORT.write([RTU_ADDRESS, 1, 0, 0, 0, 2])  # Assuming coil addresses 0 and 1 for actuators
        response = RTU_PORT.read(4)
        actuator1_value = response[3] & 1
        actuator2_value = (response[3] >> 1) & 1
        
        # Control actuators
        control_actuators(actuator1_value, actuator2_value)
        
        # Delay before the next iteration
        time.sleep(1)
        
    except KeyboardInterrupt:
        break
