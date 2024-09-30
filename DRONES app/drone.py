import socket
import threading
import time

########################################################################################################
#MACROS?
PORT = 5050
#dont forget to change that according to HOST ip 
SERVER = '192.168.1.25'
ADDR = (SERVER, PORT)
#MAX length of data that can be sent
HEADER = 32
FORMAT = 'utf-8'
#when server receive this msg from client it will disconnect it from the server
DISSCONNECT_MSG = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET for IPv4 
client.connect(ADDR) #bind our cliet with our server's address(server and port)

#global position of drone
x=0
y=0

########################################################################################################
#functions
def receive():
    while True:
        msg = client.recv(2048).decode(FORMAT)
        if msg == DISSCONNECT_MSG:
            print(f"{client} DISCONNECTED")
            client.close()
            break
        else:
            global x,y
            print(f"Received: {msg}") 
            #save gloabl x,y of the drone
            x, y = msg.split(',')  # Split the string at the comma
            x = int(x.strip())  
            y = int(y.strip())

            #send current location in case of drone misposition
            send(f"{client.getsockname()} is at ({x}, {y}))")

def send(msg):
    global x,y
    message = msg.encode(FORMAT)

    #get msg length first and pad the rest so that its size equals HEADER
    msg_len = len(message)
    send_length = str(msg_len).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))

    #send msg len first then send msg
    client.send(send_length)
    client.send(message)

    time.sleep(5)

    # #receive initial position
    # receive()

# Start the receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Start the send thread
receive_thread = threading.Thread(target=send(''))
receive_thread.start()

receive()
# make sure connection is successfull
send (f"{client.getsockname()} CONNECTED)")
