import cv2                                                                                                              					#For image processing.
import numpy as np                                                                                                      					#For matrice operations.
import math 											#For converting radians to degreesReturn the new line coordinate												#

cap=cv2.VideoCapture('LANE_VIDEO.mp4')                                                                   				#Reading the video file
while(True):											#Infinite loop.
    ret,frame=cap.read()                                                                                                					#Read the next frame of the video.
    if (ret): 												#When ret is False, the video is over.
        line_image = frame.copy() 									#Create a clone of the frame (This will be untouched).
        original = frame.copy() 										#Create a clone of the frame (To draw unprocessed lines).
        height=frame.shape[0]                                                                                              				 	#Find height(no.of rows of image).
        width=frame.shape[1]                                                                                               				 	#Find width(no.of columns in the image).
        roi_vertices=[(0,height),(width/2+55,height/2+50),(width*2/3-55,height/2+50),(width,height-200),(width,height)] 	                  #Set the region of interest (i.e. road).
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)                                                                         			#Convert BGR to grayscale image
        canny_img=cv2.Canny(gray,50,150)                                                                                   				#Apply Canny edge detection with minVal 100 and maxVal 200
        mask=np.zeros_like(canny_img)                                                                                       				#Create a zeros image of same dimension as the edge detected image
        cv2.fillPoly(mask,np.array([roi_vertices],np.int32),255)                                                            				#The polygonal area bound by the specified vertices is filled with 255(i.e. white)
        cropped_img=cv2.bitwise_and(canny_img,mask)                                                                         			#AND operation performed between edge detected image and mask to crop the image
        lines=cv2.HoughLinesP(cropped_img,rho=2,theta=np.pi/180,threshold=100,minLineLength=40,maxLineGap=5)               	#Apply probabilistic Hough Transform on the cropped edge-detected image										    
        for line in lines:                                                                                                  					#Iterating on each of the lines detected
           if line is None: 										#if no lines were detected,
               pass 											#skip this iteration.
           else: 											#If lines were detected.
               x1,y1,x2,y2=line[0]                                                                                              					#Find out the starting and ending points of the line segment
               cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),2) 							#Draw a line joining the end points.
               m = abs((y2-y1)/(x2-x1)) 										#Magnitude of the slope.
               slope_d = math.degrees(math.atan(m)) 								#Finding the slope angle in terms of degrees.
               if slope_d >=5: 										#If the slope angle is above 5 degrees.   						#Find the end points of the right line using make_points function.
                   x1,y1,x2,y2 = line[0] 									#Extract the end points. 									#Extract the end points.
                   cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),2) 							#Draw the processed line.
             								
        cv2.imshow("Lane_detection",frame)                                                                                           			#Display the Images.
        #cv2.imshow("Lines",line_image) 									#
        #cv2.imshow("POLYGONAL ROI",cropped_img) 							#
        #cv2.imshow("POLYGONAL ROI MASK",mask) 								#
        #cv2.imshow("CANNY_EDGE",canny_img) 								#
        #cv2.imshow("GRAYSCALE",gray) 									#
        #cv2.imshow("ORIGINAL",original) 									#
												#
        if cv2.waitKey(1) & 0xFF==ord('q'):                                                                                 				#Break if q is pressed
           break 											#
    else: 												#
        break 											#
cap.release()                                                                                                           					#Close the video file
cv2.destroyAllWindows()                                                                                                 					#All windows are destroyed if program is terminated
