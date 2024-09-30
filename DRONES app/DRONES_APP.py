from customtkinter import *
import station
import threading
import subprocess #to open client file here

######### TO CREATE AN EXE FILE   ##############
'''NOTE: I didn't make the app windowed beacuse the terminal shows us important info
sent and received by the drones to be sure that the data was sent successfully
but I added a small terminal in the app that shows changes in the server

unfortunately the 'drone.py' file must be present at the same folder as the exe
for the app to work (don't know how to fix this)

Another important note that in the 'drone.py' file we must change the host ip if needed
'''
#pyinstaller --onefile --icon="pilot.ico" --add-data "drone.py;." DRONES_APP.py
########################################################################################################
# Initialize window
wind = CTk()

# Start at required aspect ratio
wind.geometry('850x450')
wind.title("Control Station")
wind.resizable(True, True)

########################################################################################################
# Monitor frame (bottom-left side)
frame1 = CTkFrame(wind, width=500, height=500)
frame1.pack(side=LEFT, fill=BOTH, expand = True)

# Entries and options frame (top-right side)
frame2 = CTkFrame(wind, width=250)
frame2.pack(side=RIGHT, fill=Y)

########################################################################################################
#fonts
font1 = CTkFont(family="Courier" , size=29, weight="bold")
font2 = CTkFont(family="Courier" , size=20, weight="bold")
font3 = CTkFont(family="Courier" , size=13, weight="bold")

########################################################################################################
#funtions
def print_plane():
    txtbox.delete(0.0, END) 
    for x in range (5):
        for y in range (5):
            txtbox.insert(END, station.plane[x][y])
            if (y != 4):
                txtbox.insert(END, ' | ')
            else:
                if x != 4:
                    txtbox.insert(END, '\n')
        if (x != 4):
            txtbox.insert(END, '-----------------------\n')

def handle_connections_in_main_thread():
    #Poll the queue and handle any new connections.
    if not station.addr_queue.empty():
        conn, addr = station.addr_queue.get()
        txtbox2.insert(END, f"[NEW CONNECTION] {addr} connected.\n")
        txtbox2.insert(END, f"[ACTIVE CONNECTIONS] {station.threading.active_count()-2}\n")

    if not station.data_queue.empty():
        #get new drone cords from data queue
        x,y = station.data_queue.get()
        add_drone(x, y)
        txtbox2.insert(END, f"[DRONE POSITION] Drone at ({x}, {y})\n")
    
    # Poll every 500 milliseconds
    wind.after(500, handle_connections_in_main_thread)

def create_drone():
    # Running drone.py in a new process
    subprocess.Popen(['python', 'drone.py'])

def show_drone_data():
    drone_name = drone_number.get()

    if drone_name in drone_dict:
        x,y = drone_dict[drone_name]
        station.show_drone_data(x, y)

        if not station.data_queue.empty():
            conn, addr = station.data_queue.get()
            clear_entries()
            e1.insert(END, drone_name)
            e2.insert(END, addr[0])
            e3.insert(END, f'{x}, {y}')
            e4.insert(END, addr[1])

    else:
        txtbox2.insert(END, f"Drone {drone_name} not found.\n")


# Initialize an empty dict to store drones
drone_dict = {}
# Initialize a counter for drone names
drone_no = 1
# Function to add a drone with its position
def add_drone(x, y):
    global drone_no
    # Generate the drone name, e.g., D1, D2, D3...
    drone_name = f"D{drone_no}"
    # Store the drone's position as a tuple (x, y)
    drone_dict[drone_name] = (x, y)
    # Increment the counter for the next drone
    drone_no += 1

    station.plane[x][y] = drone_name

    #reprint plane after adding new drone
    print_plane()

def update_drone():
    old_x, old_y = e3.get().split(',')  # Split the string at the comma
    new_x = int(old_x.strip())  
    new_y = int(old_y.strip())

    drone_name = drone_number.get()
    if drone_name in drone_dict:
        old_x = drone_dict[drone_name][0]
        old_y = drone_dict[drone_name][1]
        station.show_drone_data(old_x, old_y)
        
        if not station.data_queue.empty():
            conn, addr = station.data_queue.get()
            #now we have its conn, address and the new cords
            if station.update_drone_position(conn, addr, new_x, new_y):

                # Store the drone's NEW position as a tuple (x, y)
                drone_dict[drone_name] = (new_x, new_y)

                #add drone to its new position and make the original empty
                station.plane[new_x][new_y] = drone_name
                station.plane[old_x][old_y] = 0
                
                #reprint plane after adding new drone
                print_plane()
                txtbox2.insert(END, f"updated position for drone {drone_name} to ({new_x}, {new_y}).\n")
                clear_entries()
            else:
                txtbox2.insert(END, f"Position for drone {drone_name} is already occupied.\n")

def kick_drone():
    drone_name = drone_number.get()
    if drone_name in drone_dict:
        x = drone_dict[drone_name][0]
        y = drone_dict[drone_name][1]
        station.show_drone_data(x, y)
        
        if not station.data_queue.empty():
            conn, addr = station.data_queue.get()
            station.dissconnect(conn, addr)
            #remove it from plane
            station.plane[x][y] = 0
            #remove it from dict
            del drone_dict[drone_name]
            #reprint plane after adding new drone
            print_plane()
            txtbox2.insert(END, f"Drone {drone_name} was dissconnected.\n")
            clear_entries()
    else:
        txtbox2.insert(END, f"Drone {drone_name} not found.\n")

def clear_entries():
    e1.delete('0', END)
    e2.delete('0', END)
    e3.delete('0', END)
    e4.delete('0', END)
########################################################################################################
#textbox
txtbox = CTkTextbox(frame1, font= font1, height=275)
txtbox.pack(fill=BOTH, expand=True)

txtbox2 = CTkTextbox(frame1, font= font3, height=30)
txtbox2.pack(fill=BOTH, expand=True)

########################################################################################################
#entries and labels
drone_number = StringVar()
drone_ip     = StringVar()
drone_x = StringVar()
drone_y = StringVar()

l1 = CTkLabel(frame2, text = "Choose Drone", fg_color="transparent", font=font2)
l1.grid(row = 0, column = 0, pady = 3, padx = 5)

e1 = CTkEntry(frame2, placeholder_text="", width = 175, height = 50, font=font2)
e1.configure(textvariable = drone_number)
e1.grid(row = 1, column = 0, pady = 3, padx = 3)

l2 = CTkLabel(frame2, text = "Drone's IP", fg_color="transparent", font=font2)
l2.grid(row = 0, column = 1, pady = 3, padx = 5)

e2 = CTkEntry(frame2, placeholder_text="", width = 175, height = 50, font=font2)
e2.configure(textvariable = drone_ip)
e2.grid(row = 1, column = 1, pady = 3, padx = 3)


l3 = CTkLabel(frame2, text = "X, Y (0:4)", fg_color="transparent", font=font2)
l3.grid(row = 2, column = 0, pady = 3, padx = 10)

e3 = CTkEntry(frame2, placeholder_text="", width = 175, height = 50, font=font2)
e3.configure(textvariable = drone_x)
e3.grid(row = 3, column = 0, pady = 3, padx = 3)


l4 = CTkLabel(frame2, text = "Drone's Port", fg_color="transparent", font=font2)
l4.grid(row = 2, column = 1, pady = 3, padx = 10)

e4 = CTkEntry(frame2, placeholder_text="", width = 175, height = 50, font=font2)
e4.configure(textvariable = drone_y)
e4.grid(row = 3, column = 1,pady = 3, padx = 3)

########################################################################################################
#buttons
b1 = CTkButton(frame2, text="Show Drone Data", font = font1, width = 300, height = 40)
b1.grid(row = 5, column = 0, columnspan = 2, padx = 50, pady = (50, 5))
b1.configure(command = show_drone_data)

b2 = CTkButton(frame2, text="ADD Drone", font = font1, width = 300, height = 40)
b2.grid(row = 6, column = 0, columnspan = 2, padx = 50, pady = 5)
b2.configure(command = create_drone)

b3 = CTkButton(frame2, text="Update Drone", font = font1, width = 300, height = 40)
b3.grid(row = 7, column = 0, columnspan = 2, padx = 50, pady = 5)
b3.configure(command = update_drone)

b4 = CTkButton(frame2, text="Remove Drone", font = font1, width = 300, height = 40)
b4.grid(row = 8, column = 0, columnspan = 2, padx = 50, pady = 5)
b4.configure(command = kick_drone)

########################################################################################################
#main
#starting a thread to start the connection while the app loop is still running
thread2 = threading.Thread(target= station.start_connection)
thread2.start()


# Poll for new connections in the queue using after()
handle_connections_in_main_thread()

''' 
in the station file we made the threading '-1' which is the thread of the station
now we will make it '-2' for the  extra thread here for the app's loop
'''
txtbox2.insert(END, f'[STARTING] server starting at {station.SERVER}\n')
txtbox2.insert(END, f'[ACTIVE CONNECTIONS] {station.threading.active_count()-2}\n')
print_plane()

# Start the main loop
wind.mainloop()