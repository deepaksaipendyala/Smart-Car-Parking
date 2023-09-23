# Smart-Car-Parking using SCADA Network

## **Objective**:
- Develop a smart vehicle parking system using sensors to detect available slots.
- Display the best available slots to drivers.
- Implement and control the system over a SCADA network system.

## **Abstract**:
- Use sensors to detect available parking slots.
- Send this information to a central server.
- The server processes the data and communicates with a Pico at the entrance, which displays the available slots.
- Drivers can select a slot, and the Pico communicates this back to the server for database updating.

## **System Overview**:
- A Supervisory Control and Data Acquisition (SCADA) system is used.
- Central server: Laptop.
- Remote clients: Two Raspberry Pico with four IR sensors each.
- Real-time monitoring and control of parking slots.
- The server acts as the central control, while clients collect and send data.

## **Methodology**:
### **Socket Programming**:
- Used to set up the SCADA master. Multithreading connects two clients to the server.
### **Client-Side**:
  - Raspberry Pico monitors parking slots using the IR sensor.
  - Sends real-time data to the server and later receives data for parking slot allocation.
### **Server-Side**:
  - Laptop-based server application processes data.
  - Implements real-time monitoring and controlling features.
### **Communication**:
  - WebSocket connections established between clients and server.
  - Data Transmission: Clients send parking slot data to the server.
  - Slot Detection: Clients monitor and report on slot allocation and availability.

## **Implementation**:
- Server application is set up using socket programming.
- Multithreading allows concurrent client handling.
- Empty slots detected using IR sensors.
- Slot information communicated to the SCADA master.
- Data is processed and communicated between the server, Pico at the entrance, and Pico in the parking area.
- Gate control and LED displays are managed through the system.
- Data updates (e.g., car entry, time, slot) are managed in the database and GUI.

## **Process Flow**:
![Fig 1](./images/CNIC%20flow.png)
1. Vehicle approaches the Pico at the entry gate.
2. SCADA master communicates with Pico in the parking area.
3. Available parking slots are displayed at the entrance.
4. Slot availability is communicated back to the server.
5. Process continues until all slots are filled. If full, “NO SLOTS AVAILABLE” is displayed.

## **Results**:
### **Server Output** ###
- ![Fig 1](images/Fig%201%20Server%20Output.png)
### **Client 1 Output** ###
- ![Fig 2](images/Fig%202%20Client%201%20Output.png)
### **Client 2 Output** ###
- ![Fig 3](images/Fig%203%20Client%202%20Output.png)
### ** GUI Output** ###
- ![Fig 4](images/Fig%204%20GUI%20Output.png)
### **Stored Data from Server** ###
- ![Fig 6](images/Fig%206%20Data%20which%20is%20stored%20from%20server.png)

## **Conclusion**:
- Effective real-time monitoring system using a client-server architecture.
- Seamless communication enabled through socket programming.
- Continuous real-time data provided by clients to the server.
- Efficient and user-friendly system design.
- Scalability for larger parking lots.
