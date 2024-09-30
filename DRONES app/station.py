import socket
import threading
import queue  # Import Queue for sharing data

# Queue to store the connection data
addr_queue = queue.Queue()
data_queue = queue.Queue()
########################################################################################################
#MACROS?
PORT = 5050
'''
instead of hard coding the ip address of the host 
"socket.gethostbyname" function gets it autmatically for us
'''
SERVER = socket.gethostbyname(
    socket.gethostname())
ADDR = (SERVER, PORT)
#MAX length of data that can be sent
HEADER = 32
FORMAT = 'utf-8'
#when server receive this msg from client it will disconnect it from the server
DISSCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET for IPv4 
server.bind(ADDR) #bind our sever with our address(server and port)

########################################################################################################
#data
plane = [[0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]]

class Drone:
    def __init__(self, connection, address, x, y):
        self.connection = connection
        self.address = address
        self.x = x
        self.y = y

#list to stores drones (as classes)
drones = []

# Function to check if a position (x, y) is already occupied
def is_position_occupied(x, y):
    for drone in drones:
        if drone.x == x and drone.y == y:
            return True
    return False

# Function to find an available position
def find_available_position():
    for x in range(5):
        for y in range(5):
            if not is_position_occupied(x, y):
                return x, y
    return None  # If no positions are available
########################################################################################################
#functions
def start_connection():
    #listening to any client wanting to connect to our server
    server.listen()
    #wait for new connection to occur
    while True:
        #conn is stored object of client
        #addr is the address (ip, port) of client
        conn, addr = server.accept()

        # Put data into the queue so the app thread can access it
        addr_queue.put((conn, addr))

        #starting  a thread to make the loop work along side the rest of the code
        thread = threading.Thread(target= handle_drone, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-2}") #for the app loop 
        

def handle_drone(conn, addr):
    print (f"[NEW CONNECTION] {addr} connected.\n")

    # Assign default new position or find an available one
    if not is_position_occupied(0, 0):
        new_drone = Drone(conn, addr, 0, 0)
        print(addr)
        #return its position
        curr_x = 0
        curr_y = 0
    else:
        available_position = find_available_position()
        if available_position:
            new_drone = Drone(conn, addr, available_position[0], available_position[1])
            curr_x = available_position[0]
            curr_y = available_position[1]
        else:
            print(f"No available positions for drone {addr}.")
            conn.close()  # Close connection if no position is available
            return
        
    # Append new drone to the drones list
    drones.append(new_drone)  
    #send initial position to app
    data_queue.put((curr_x, curr_y))
    
    connected = True
    #wait to receive info from client
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT).strip()
        if msg_len: #if it is not an empty string
            msg_len = int(msg_len)
            #recevie actuall msg
            msg = conn.recv(msg_len).decode(FORMAT)

            #disconnect client if dissconnect msg is sent
            if msg == DISSCONNECT_MSG:
                connected = False

            #for testing
            print(f"{addr} sent {msg}")
            
            #send its position
            msg2 = f'{curr_x}, {curr_y}'
            conn.send(msg2.encode(FORMAT))  # Then send the actual message


    conn.close()

def update_drone_position(conn, addr, new_x, new_y):
    for drone in drones:
        #make sure we are changing the right drone's data
        if drone.address == addr:
            #make sure it is free
            if not is_position_occupied(new_x, new_y):
                drone.x = new_x
                drone.y = new_y

                #send new position to drone
                msg = f'{new_x}, {new_y}'
                conn.send(msg.encode(FORMAT))  # Then send the actual message
                return 1
            
            else:
                print(f"Position for drone {addr} is already occupied.")
                return 0

def show_drone_data(x,y):
    for drone in drones:
        if drone.x == x and drone.y == y:
            #put its cords in queue
            data_queue.put((drone.connection, drone.address))
        
def dissconnect(conn, addr):
    for drone in drones:
        #make sure we are changing the right drone's data
        if drone.address == addr:
            conn.send(DISSCONNECT_MSG.encode(FORMAT))
            #remove it from list
            drones.remove(drone)

########################################################################################################
#main
print(f"[STARTING] server is starting at {SERVER}")
print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")