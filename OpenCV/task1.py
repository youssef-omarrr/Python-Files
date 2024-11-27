import cv2 as cv
import numpy as np
from customtkinter import *

#setup window to get initial data
class SetupWindow(CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Setup Canvas")
        self.geometry("350x300")
        
        #to store the color and dimensions
        self.result = None  

        #font for labels and buttons
        font1 = CTkFont(family="Courier", size=20, weight="bold")
        font2 = CTkFont(family="Courier", size=10)

        #color data
        self.color = StringVar()

        l0 = CTkLabel(self, text="*if you presses the button without adding data \nit will give you the default settings*", font=font2)
        l0.pack(pady=2)
        
        l1 = CTkLabel(self, text="Canvas Color (B,G,R)", font=font1)
        l1.pack(pady=7)

        self.color_entry = CTkEntry(self, textvariable=self.color, font=font1, width=200, height=40)
        self.color_entry.pack(pady=5)

        #dimensions data
        self.dim = StringVar()

        l2 = CTkLabel(self, text="Dimensions (WxH)", font=font1)
        l2.pack(pady=7)

        self.dim_entry = CTkEntry(self, placeholder_text="650x500", textvariable=self.dim, font=font1, width=200, height=40)
        self.dim_entry.pack(pady=5)

        #create button
        self.update_button = CTkButton(self, text="Create Canvas", font=font1, width=200, height=40, command=self.create_canvas)
        self.update_button.pack(pady=7)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_canvas(self):
        # Get the values from the entries
        color = self.color.get() or "255,255,255"  #default color
        dimensions = self.dim.get() or "850x850"   #default dimensions
        
        # Parse the color input ("255,25,0" => (255, 25, 0))
        color = tuple(map(int, color.split(',')))

        # Parse the dimensions input ("850x850" => 850, 850)
        width, height = map(int, dimensions.split('x'))

        #init opencv canvas
        self.result = color, width, height
        
        # Close the setup window
        self.destroy()
        
    def on_close(self):
        self.result = None
        self.destroy()
        
#############################################################################################
#############################################################################################
#############################################################################################
        
class PainterApp:
    def __init__(self, color, width, height):
                
        #create the opencv canvas
        self.CVcanvas = np.full((height, width, 3), color, dtype=np.uint8)
        cv.imshow("Canvas", self.CVcanvas)  # Show the canvas window
        
        #canvas parameters
        self.drawing = False 
        self.mode = None #circle, rect, poly, erase, etc
        self.start_x = -1
        self.start_y = -1
        self.polygon_points = []
        self.cropping_points = []
        self.canvColor = color
        
        #line color
        self.colorCircle = (95, 13, 100)
        self.colorRect   = (120, 116, 56) 
        self.colorPoly   = (0, 178, 255)
    
        #canvas running or closed
        self.running = True
        
        # Undo/Redo stacks
        self.undo_stack = []
        self.redo_stack = []
        
        #add initial canvas state to undo stack
        self.make_change(self.CVcanvas.copy())
        
        #handle mouse events
        cv.setMouseCallback("Canvas", self.mouse_callback)  
        
#############################################################################################

    def push_to_undo(self, canvas):
        #push canvas state to the undo stack
        self.undo_stack.append(canvas)

    def push_to_redo(self, canvas):
        #push canvas state to the redo stack
        self.redo_stack.append(canvas)

    def undo(self):
        #there is something to undo
        if len(self.undo_stack) > 1: 
            #save the current canvas to redo stack
            self.push_to_redo(self.undo_stack.pop())  
            
            #get the previous canvas state
            self.CVcanvas = self.undo_stack.pop()
            
            cv.imshow("Canvas", self.CVcanvas)
            self.push_to_undo(self.CVcanvas.copy()) 
            print("Undo")
        else:
            print("Nothing to UNDO")

    def redo(self):
        #there is something to redo
        if self.redo_stack:
            redo_canvas = self.redo_stack.pop()
            self.CVcanvas = redo_canvas
            cv.imshow("Canvas", self.CVcanvas)
            self.push_to_undo(self.CVcanvas.copy()) 
            print("Redo")
        else:
            print("Nothing to REDO")
            
    def make_change(self, new_canvas_state):
        #when a new change is made, push the current state to undo and CLEAR redo stack
        self.push_to_undo(new_canvas_state)
        #clear redo stack when a new change happens
        self.redo_stack.clear() 

#############################################################################################

    def key_event_loop(self):
        while self.running:
            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
                cv.destroyAllWindows()
                break
            self.key_press_handler(key)
            
    def on_closing(self):
        self.running = False
        cv.destroyAllWindows()
    
##########__________________################_______________##############_____________############

    def mouse_callback(self, event, x, y, flags, param):
        if self.mode == "circle":
            if event == cv.EVENT_LBUTTONDOWN:
                self.start_x, self.start_y = x, y
                self.drawing = True
                
            elif event == cv.EVENT_MOUSEMOVE and self.drawing:
                radius = int(((x - self.start_x)**2 + (y - self.start_y)**2)**0.5)
                self.CVcanvas_copy = self.CVcanvas.copy()
                cv.circle(self.CVcanvas_copy, (self.start_x, self.start_y), radius, self.colorCircle, 2)
                cv.imshow("Canvas", self.CVcanvas_copy)
                
            elif event == cv.EVENT_LBUTTONUP:
                self.drawing = False
                cv.circle(self.CVcanvas, (self.start_x, self.start_y), 
                          int(((x - self.start_x)**2 + (y - self.start_y)**2)**0.5), self.colorCircle, 2)
                cv.imshow("Canvas", self.CVcanvas)
                self.make_change(self.CVcanvas.copy())

##########__________________################_______________##############_____________############

        elif self.mode == "rectangle":
            if event == cv.EVENT_LBUTTONDOWN:
                self.start_x, self.start_y = x, y
                self.drawing = True
                
            elif event == cv.EVENT_MOUSEMOVE and self.drawing:
                self.CVcanvas_copy = self.CVcanvas.copy()
                cv.rectangle(self.CVcanvas_copy, (self.start_x, self.start_y), (x, y), self.colorRect, 2)
                cv.imshow("Canvas", self.CVcanvas_copy)
                
            elif event == cv.EVENT_LBUTTONUP:
                self.drawing = False
                cv.rectangle(self.CVcanvas, (self.start_x, self.start_y), (x, y), self.colorRect, 2)
                cv.imshow("Canvas", self.CVcanvas)
                self.make_change(self.CVcanvas.copy())

                
##########__________________################_______________##############_____________############

        elif self.mode == "polygon":
            if event == cv.EVENT_LBUTTONDOWN:
                #add a new point
                self.polygon_points.append((x, y))
                self.CVcanvas_copy = self.CVcanvas.copy()
                
                #add a circle at the point
                for i in range(len(self.polygon_points)):
                    cv.circle(self.CVcanvas_copy, self.polygon_points[i], 5, self.colorPoly, -1)
                    
                #draw lines between points
                if len(self.polygon_points) > 1:
                    cv.polylines(self.CVcanvas_copy, [np.array(self.polygon_points)], False, self.colorPoly, 2)
                    
                cv.imshow("Canvas", self.CVcanvas_copy)

                
##########__________________################_______________##############_____________############

        elif self.mode == "erase":
            if event == cv.EVENT_LBUTTONDOWN:
                self.start_x, self.start_y = x, y
                self.drawing = True
                
            elif event == cv.EVENT_MOUSEMOVE and self.drawing:
                self.CVcanvas_copy = self.CVcanvas.copy()
                eraser_size = 20  # Fixed-size square eraser
                cv.rectangle(self.CVcanvas_copy, (x - eraser_size // 2, y - eraser_size // 2),
                            (x + eraser_size // 2, y + eraser_size // 2), self.canvColor, -1)
                cv.imshow("Canvas", self.CVcanvas_copy)
                self.make_change(self.CVcanvas.copy())

                
            elif event == cv.EVENT_LBUTTONUP:
                self.drawing = False
                eraser_size = 20  # Fixed-size square eraser
                cv.rectangle(self.CVcanvas, (x - eraser_size // 2, y - eraser_size // 2),
                            (x + eraser_size // 2, y + eraser_size // 2), self.canvColor, -1)
                cv.imshow("Canvas", self.CVcanvas)
                self.make_change(self.CVcanvas.copy())

                
##########__________________################_______________##############_____________############

        elif self.mode == "crop":
            if event == cv.EVENT_LBUTTONDOWN:
                self.CVcanvas_copy = self.CVcanvas.copy()
                self.cropping_points.append((x, y))
                
                cv.circle(self.CVcanvas_copy, self.cropping_points[len(self.cropping_points)-1], 5, (0,0,0), -1)
                cv.imshow("Canvas", self.CVcanvas_copy)
                
                if len(self.cropping_points) == 4:
                    x1, y1 = self.cropping_points[0]
                    x2, y2 = self.cropping_points[2]
                    cropped_self = self.CVcanvas[y1:y2, x1:x2]
                    cv.imshow("Cropped canvas (CLOSE IT BEFORE CROPPING AGAIN!!!)", cropped_self)
                    self.cropping_points = []
                    cv.imshow("Canvas", self.CVcanvas)
                
                if len(self.cropping_points) > 4:
                    print("Error in croping try again")
                    self.cropping_points = []
                    
#############################################################################################

    def key_press_handler(self, key):
        if key == ord('c'):
            self.mode = "circle"
            print("Circle Mode Activated")
            
        elif key == ord('r'):
            self.mode = "rectangle"
            print("Rectangle Mode Activated")
            
        elif key == ord('p'):
            self.mode = "polygon"
            self.polygon_points = []
            print("Polygon Mode Activated")
            
        elif key == ord('e'):
            self.mode = "erase"
            print("Erase Mode Activated")
            
        elif key == ord('x'):
            self.mode = "crop"
            self.cropping_points = []
            print("Cropping Mode Activated")
            
        elif key == ord('s') and self.mode == "polygon":
            self.mode = None
            if len(self.polygon_points) > 1:
                #draw a line between the first and last points
                cv.line(self.CVcanvas_copy, self.polygon_points[0], self.polygon_points[-1], self.colorPoly, 2)
                self.CVcanvas = self.CVcanvas_copy
                
                #show the updated canvas
                cv.imshow("Canvas", self.CVcanvas)
                self.make_change(self.CVcanvas.copy())
                
                self.polygon_points = []
 
                print("Polygon Drawn")
                
            else:
                print("Not enough points to draw a polygon")
            
        elif key == ord('a'):
            self.mode = "rotate_right"
            print("Rotate Right")
            
        elif key == ord('d'):
            self.mode = "rotate_left"
            print("Rotate Left")
            
        elif key == ord('['):
            if self.mode == "polygon":
                print("Can't undo when in poly mode")
            else:
                self.undo()  
            
        elif key == ord(']'):
            if self.mode == "polygon":
                print("Can't redo when in poly mode")
            else:
                self.redo() 
            
        if self.mode == "rotate_right":
            self.CVcanvas = cv.rotate(self.CVcanvas, cv.ROTATE_90_CLOCKWISE)
            self.make_change(self.CVcanvas.copy())
            cv.imshow("Canvas", self.CVcanvas)
            self.mode = None
            
        elif self.mode == "rotate_left":
            self.CVcanvas = cv.rotate(self.CVcanvas, cv.ROTATE_90_COUNTERCLOCKWISE)
            self.make_change(self.CVcanvas.copy())
            cv.imshow("Canvas", self.CVcanvas)
            self.mode = None
        
#############################################################################################
# Run the app
if __name__ == "__main__":
    set_appearance_mode("dark")

    app = CTk()
    setup_window = SetupWindow(master=app)

    #wait for the setup window to close
    app.wait_window(setup_window)

    #get the result data from the setup window
    if setup_window.result:
        color, width, height = setup_window.result
        painter = PainterApp(color, width, height)
        
        app.destroy()  #close the root ctk app
        painter.key_event_loop()
        
    else:
        print("Setup canceled. Exiting.")
        app.destroy()