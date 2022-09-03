import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import imutils

def read_letters(img_):
   
    pytesseract.pytesseract.tesseract_cmd=r'c:/Program Files/Tesseract-OCR/tesseract.exe'
    print(pytesseract.image_to_string(img_))

    ##Detecting characters
    hImg,wImg,channel = img_.shape
    boxes = pytesseract.image_to_boxes(img_)#x,y,width,height
    for b in boxes.splitlines():
        b = b.split(' ')
        print(b)
        x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])

        cv2.rectangle(img_,(x,hImg-y),(w,hImg-h),(0,0,255),3)   
        cv2.putText(img_,b[0],(x,hImg-y+25),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)
        
    
    
    cv2.namedWindow("Result",cv2.WINDOW_NORMAL)
    cv2.imshow("Result",img_)
    cv2.waitKey(0)
    return i
imag_path = 'warped_image.jpeg'
Original1 = cv2.imread(imag_path,1)

read_letters(Original1)




