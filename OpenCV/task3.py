import cv2 as cv

class Shape_detector:
    def __init__ (self, img_name):
        self.img_name = img_name
        self.img = cv.imread(self.img_name)
        
        #rescale img
        self.img = cv.resize(self.img, (1000, 800))
        
        #change it to gray scale 
        self.img_gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY) 
        
        #add more details
        _, self.imgbin = cv.threshold(self.img_gray, 100, 255, cv.THRESH_BINARY)

        #draw lines
        contours , _ = cv.findContours(self.imgbin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(self.img, contours, -1, (46, 46, 198), 3)

        for contour in contours:
            #to approximate the number of contour to the number of sides:
            #to calculate the length of contour
            length = 0.01 * cv.arcLength(contour, True) 
            #to approximate the length of contour
            approx = cv.approxPolyDP(contour, length, True) 
            
            #for testing
            # print(len(approx)) 
            
            #Triangle
            if len(approx) == 3:
                shape = "triangle"
                self.draw_shape(approx, shape, (255, 234, 235))

            #Quadrilateral
            elif len(approx) == 4: 
                #can be square or rectangle so we need to check for hight/length ratio
                x,y,w,h = cv.boundingRect(approx)
                ratio = w/h
                
                if 0.9 <= ratio <= 1.1: 
                    shape = "square"
                    self.draw_shape(approx, shape, (103, 106, 0))
                else:
                    shape = "rectangle"
                    self.draw_shape(approx, shape, (103, 106, 0))

            #Pentagon
            elif len(approx) == 5:
                shape = "penta"

            #Hexagon
            elif len(approx) == 6:
                shape = "hexa"

            else: #any more will be considered as a circle
                shape = "circle"
                self.draw_shape(approx, shape, (97, 49, 0))

            
    def draw_shape(self, approx, shape, color):
        cv.drawContours(self.img, approx, -1, (244, 146, 13), 10)
        x,y = approx[0][0] #cords of contours 
        font = cv.FONT_HERSHEY_TRIPLEX
        if shape == "triangle":
            cv.putText(self.img, shape, (x+10,y-5), font, 1, (0,0,0), 3, cv.LINE_AA)
            
        cv.putText(self.img, shape, (x+10,y-5), font, 1, color, 2, cv.LINE_AA)
        
    def show_shape_name(self):
        cv.imshow("Task 3 shapes names", self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    def show_shape_corners(self):
        corners = cv.goodFeaturesToTrack(self.imgbin, 100, 0.01, 80)
        corners = corners.astype(int)
        for corner in corners:
            x,y = corner.ravel()
            cv.circle(self.img, (x,y), 7, (120, 191, 114), -1)
            
        cv.imshow("TASK 3 shapes corners", self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
        
if __name__ == "__main__":
    wind = Shape_detector("testSHAPES.jpg")
    wind.show_shape_name()
    wind.show_shape_corners()
    
    