import numpy as np 
import cv2 as cv

class Video:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        
        #store dimensions
        self.width = int(self.cap.get(3))
        self.height = int(self.cap.get(4))
        print(f"Video initialized: {self.width}x{self.height}")
        self.frame = None
        
        #for recording
        self.recording = False
        self.rec = None
        self.file_number = 1 #for unique file naming
        
        #for drawing 
        self.mode = None
        self.drawing = False 
        self.start_x = -1
        self.start_y = -1
        self.polygon_points = []
        
        #shape drawer instance 
        self.shape_drawer = ShapeDrawer()
        
        #line color
        self.colorCircle = (95, 13, 100)
        self.colorRect   = (120, 116, 56) 
        self.colorPoly   = (0, 178, 255) 
        
        cv.namedWindow("Video Painter") #to prevent null pointer to an unintialized window
        cv.setMouseCallback("Video Painter", self.mouse_callback)
        
##########__________________################_______________##############_____________############
    def mouse_callback(self, event, x, y, flags, param):
        if self.mode == "circle":
            if event == cv.EVENT_LBUTTONDOWN:
                self.start_x, self.start_y = x, y
                self.drawing = True

            elif event == cv.EVENT_MOUSEMOVE and self.drawing:
                temp_frame = self.frame.copy()
                radius = int(((x - self.start_x) ** 2 + (y - self.start_y) ** 2) ** 0.5)
                cv.circle(temp_frame, (self.start_x, self.start_y), radius, self.colorCircle, 2)
                cv.imshow("Video Painter", temp_frame)

            elif event == cv.EVENT_LBUTTONUP:
                self.drawing = False
                radius = int(((x - self.start_x) ** 2 + (y - self.start_y) ** 2) ** 0.5)
                self.shape_drawer.add_shape(("circle", (self.start_x, self.start_y), radius, self.colorCircle))
                self.shape_drawer.make_change(self.shape_drawer.shapes.copy())
                
##########__________________################_______________##############_____________############

        elif self.mode == "rectangle":
            if event == cv.EVENT_LBUTTONDOWN:
                self.start_x, self.start_y = x, y
                self.drawing = True

            elif event == cv.EVENT_MOUSEMOVE and self.drawing:
                temp_frame = self.frame.copy()
                cv.rectangle(temp_frame, (self.start_x, self.start_y), (x, y), self.colorRect, 2)
                cv.imshow("Video Painter", temp_frame)

            elif event == cv.EVENT_LBUTTONUP:
                self.drawing = False
                self.shape_drawer.add_shape(("rectangle", (self.start_x, self.start_y), (x, y), self.colorRect))
                self.shape_drawer.make_change(self.shape_drawer.shapes.copy())
                
##########__________________################_______________##############_____________############

        elif self.mode == "polygon":
            if event == cv.EVENT_LBUTTONDOWN:
                #add a new point
                self.polygon_points.append((x, y))
                temp_frame = self.frame.copy()
                
                #add a circle at the point
                for i in range(len(self.polygon_points)):
                    cv.circle(temp_frame, self.polygon_points[i], 5, self.colorPoly, -1)
                    
                #draw lines between points
                if len(self.polygon_points) > 1:
                    cv.polylines(temp_frame, [np.array(self.polygon_points)], False, self.colorPoly, 2)
                    
                self.shape_drawer.add_shape(("polyPoints", vid.polygon_points.copy(), vid.colorPoly))
                cv.imshow("Video Painter", temp_frame)
##########__________________################_______________##############_____________############

    def start_video(self):
        print("Starting video...")
        while True:
            ret, self.frame = self.cap.read()
            if not ret:
                break
            
            #draw shapes on the current frame
            shapes_frame = self.frame.copy()
            self.shape_drawer.draw(shapes_frame)
            
            self.frame = shapes_frame
            cv.imshow("Video Painter", self.frame)
            
            #write the frame if recording
            if self.recording and self.rec:
                self.rec.write_frame(self.frame)
            
            key = cv.waitKey(1) & 0xFF
            if key == ord('q'): #quit the program
                break
            key_press_handler(key)
            
            
        self.stop_video()
    
    def stop_video(self):
        print("Stopping video...")
        self.cap.release()
        cv.destroyAllWindows()
        
#############################################################################################

class Recording:
    def __init__(self, filename, width, height, frame, fps = 20.0):
        self.filename = filename
        self.width = width
        self.height = height
        self.frame = frame
        
        self.is_paused = False
    
        fourcc = cv.VideoWriter_fourcc(*'XVID')  #Codec (compress and decompress video data) for .avi files
        self.video_writer =  cv.VideoWriter(self.filename, fourcc, fps, (self.width, self.height))
        
        print(f"Initialized recording: {self.filename}")
        
    def write_frame(self, frame):
        #write the current frame to te recorded video
        if not self.is_paused:
            self.video_writer.write(frame)
        
    def pause_rec(self):
        self.is_paused = True
    
    def resume_rec(self):
        self.is_paused = False
    
    def stop_rec(self):
        self.video_writer.release()
        print(f"Recording saved: {self.filename}")
        
#############################################################################################

def key_press_handler(key):
    if key == ord('m'): #start recording
        if not vid.recording:
            filename = F"testVideo{vid.file_number}.avi"
            vid.recording = True
            vid.rec = Recording(filename, vid.width, vid.height, vid.frame)
            print(f"Recording started: {filename}")
            vid.file_number += 1
            
    elif key == ord(','): #pause recording
        if vid.recording and vid.rec:
            vid.rec.pause_rec()
            vid.recording = False
            print("Recording paused.")
        
    elif key == ord('.'): #resume recording
        if not vid.recording and vid.rec:
            vid.rec.resume_rec()
            vid.recording = True
            print("Recording resumed.")
    
    elif key == ord('/'): #stop recording
        if vid.recording and vid.rec:
            vid.rec.stop_rec()
            vid.recording = False
            print("Recording stopped.")
            
    elif key == ord('c'):
        vid.mode = "circle"
        print("Circle Mode Activated")

    elif key == ord('r'):
        vid.mode = "rectangle"
        print("Rectangle Mode Activated")

    elif key == ord('p'):
        vid.mode = "polygon"
        vid.polygon_points = []
        print("Polygon Mode Activated")
        
    elif key == ord('s') and vid.mode == "polygon":
        vid.mode = None
        if len(vid.polygon_points) > 1:
            vid.shape_drawer.add_shape(("polygon", vid.polygon_points.copy(), vid.colorPoly))
            vid.shape_drawer.remove_shape(("polyPoints", vid.polygon_points.copy(), vid.colorPoly))
            
            vid.shape_drawer.make_change(vid.shape_drawer.shapes.copy())
            
            #show the updated canvas
            cv.imshow("Video Painter", vid.frame)
            vid.polygon_points = []

            print("Polygon Drawn")
            
        else:
            print("Not enough points to draw a polygon")
            
    elif key == ord('['):
        if vid.mode == "polygon":
            print("Can't undo when in poly mode")
        else:
            vid.shape_drawer.undo()  
        
    elif key == ord(']'):
        if vid.mode == "polygon":
            print("Can't redo when in poly mode")
        else:
            vid.shape_drawer.redo() 


#############################################################################################

class ShapeDrawer:
    def __init__(self):
        #to store shapes and thier data as tuples
        self.shapes = []  
        self.undo_stack = []
        self.redo_stack = []
        
        #add inital shapes state to undo stack
        self.make_change(self.shapes.copy())

    def add_shape(self, shape_type, *args):
        #add a shape to the shapes list
        self.shapes.append(shape_type, *args)

    def draw(self, frame):
        #draw all shapes onto the frame
        for shape in self.shapes:
            if shape[0] == "circle":
                garbage, center, radius, color = shape
                cv.circle(frame, center, radius, color, 2)
                
            elif shape[0] == "rectangle":
                garbage, pt1, pt2, color = shape
                cv.rectangle(frame, pt1, pt2, color, 2)
                
            elif shape[0] == "polygon":
                garbage, points, color = shape
                for i in range(len(points)):
                    cv.circle(frame, points[i], 5, color, -1)
                    
                cv.polylines(frame, [np.array(points)], True, color, 2)
                cv.line(frame, points[0], points[-1], color, 2)
                
            elif shape[0] == "polyPoints":
                garbage, points, color = shape
                for i in range(len(points)):
                    cv.circle(frame, points[i], 5, color, -1)
                    
                #draw lines between points
                if len(points) > 1:
                    cv.polylines(frame, [np.array(points)], False, color, 2)

##########__________________################_______________##############_____________############

    def remove_shape(self, shape_type, *args):
        shape_to_remove = (shape_type, *args)
        self.shapes.remove(shape_to_remove[0])
        
    def push_to_undo(self, shapes):
        #push shapes list to the undo stack
        self.undo_stack.append(shapes)

    def push_to_redo(self, shapes):
        #push shapes list to the redo stack
        self.redo_stack.append(shapes)

    def undo(self):
        #there is something to undo
        if len(self.undo_stack) > 1: 
            #save the current shapes list to redo stack
            self.push_to_redo(self.undo_stack.pop().copy())  
            
            #get the previous shapes list state
            self.shapes = self.undo_stack[-1].copy()
            print("Undo")
        else:
            print("Nothing to UNDO")

    def redo(self):
        #there is something to redo
        if self.redo_stack:
            redo_shapes = self.redo_stack.pop().copy()
            self.shapes = redo_shapes.copy()
            self.push_to_undo(self.shapes.copy()) 
            print("Redo")
        else:
            print("Nothing to REDO")
            
    def make_change(self, new_shapes):
        new_shapes = self.shapes.copy()
        #when a new change is made, push the current state to undo and CLEAR redo stack
        self.push_to_undo(new_shapes.copy())
        #clear redo stack when a new change happens
        self.redo_stack.clear() 

#############################################################################################

if __name__ == "__main__":
    vid = Video()
    vid.start_video()
    