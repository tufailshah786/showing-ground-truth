import numpy as np
import cv2
import math  
import os
import xml.etree.ElementTree as ET
    
i=0    
def rotate_point(pointX, pointY, originX, originY, angle):
     angle = -angle
    	
     new_x = math.cos(angle) * (pointX-originX) + math.sin(angle) * (pointY-originY) + originX
     new_y = - math.sin(angle) * (pointX-originX) + math.cos(angle) * (pointY-originY) + originY
    	
     if(new_x < 0):
    		new_x = 0
     elif(new_y<0):
    		new_y=0

     return int( new_x ), int (new_y)
def draw_rotated_rectangle(img, x1y1, x1y2, x2y1, x2y2 ):
     cv2.polylines(img,[np.array([(x1y1),(x2y1),(x2y2),(x1y2)])],True,(0,255,255),5)     
for filename in os.listdir("C:/ground-truth/test/"): 
    filename=os.path.splitext(os.path.basename(filename))[0]
    tree = ET.parse("C:/ground-truth/test/"+filename+'.xml')
    root = tree.getroot()
    img = cv2.imread("C:/ground-truth/test/"+filename + ".jpg")
    for objects in tree.iter('object'):
       for doc in objects.findall('robndbox'):
        xc=float(doc.find('cx').text)
        yc=float(doc.find('cy').text)
        width=float(doc.find('w').text)
        height=float(doc.find('h').text)
        angle=float(doc.find('angle').text)
        
        x1= (xc-(width/2))
        y1 = (yc-(height)/2)
        x2= (xc+(width/2))
        y2 = (yc+(height)/2)

        x1y1 = rotate_point(x1,y1, xc, yc, angle)
        x2y2 = rotate_point(x2,y2, xc, yc, angle)
        x1y2 = rotate_point(x1,y2, xc, yc, angle)
        x2y1 = rotate_point(x2,y1, xc, yc, angle)
        draw_rotated_rectangle(img, (x1y1), (x1y2), (x2y1), (x2y2))
        cv2.imwrite("C:/ground-truth/test/"+filename + "G.jpg",img)
        print(filename+"G created")
    i +=1
