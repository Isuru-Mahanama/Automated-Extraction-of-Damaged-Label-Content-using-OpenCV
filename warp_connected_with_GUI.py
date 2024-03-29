import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
import pytesseract

def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1500:
            peri = cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i,0.015*peri,True)
            if area > max_area and len(approx) <= 15:
                biggest = approx
                max_area = area
    return biggest

def warping(name):

    img = cv2.imread(name,1)
    img1 = img.copy()
    print(img.shape[0])#512#1000
    print(img.shape[1])#384#572
    if(img.shape[0] > 1000):
        img = imutils.resize(img, width=500 )#500
    
        if(img.shape[0] > img.shape[1]):
            if(img.shape[0] < 700 and img.shape[0] > 350):
                img = cv2.resize(img,(430,530),interpolation = cv2.INTER_AREA)#400,500#430,530
            else:
                img = cv2.resize(img,(400,500),interpolation = cv2.INTER_AREA)
        
    img_original = img.copy()
    img2 = img.copy()
    #laplaciian
    
    #img = cv2.Laplacian(img,cv2.CV_8U,ksize = 3)
    # Image modification
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##    cv2.imshow('Gray',gray)
    gray = cv2.bilateralFilter(gray,20,30,30)#10,20
    edged = cv2.Canny(gray,10,20)
    #ret,edged = cv2.threshold(gray,1,255,0)

    # contour detection
    contours,hierarchy = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print("Number of contours = "+ str(len(contours)))
    contours = sorted(contours,key = cv2.contourArea,reverse = True) [:10]

    biggest =  biggest_contour(contours)
    print(len(biggest))
    #for i in contours:
    cv2.drawContours(img,[biggest],-1,(0,255,0),3)

##    cv2.imshow('Image with countours',img)


    if (len(biggest) == 4):
        #only the original image has three channels
        points = biggest.reshape(4,2)
        input_points = np.zeros((4,2),dtype = "float32")


        points_sum = points.sum(axis =1)
        input_points[0] = points[np.argmin(points_sum)]
        input_points[3] = points[np.argmax(points_sum)]

        points_diff = np.diff(points,axis = 1)
        input_points[1] =points[np.argmin(points_diff)]
        input_points[2] = points[np.argmax(points_diff)]

        (top_left,top_right,bottom_right,bottom_left)= input_points
        bottom_width = np.sqrt((bottom_right[0] - bottom_left[0]) **2) +((bottom_right[1] - bottom_left[1]) **2)
        top_width = np.sqrt(((top_right[0] - top_left[0])**2) + ((top_right[1] - top_left[1]) **2))
        right_height = np.sqrt(((top_right[0] - bottom_right[0] )**2) +((top_right[1] - bottom_right[1] )**2) )
        left_height = np.sqrt(((top_left[0] - bottom_left[0] )**2) +((top_left[1] - bottom_left[1] )**2) )


    #out_put iamge size
        max_width = max(int(bottom_width),int(top_width))

        max_height = int(max_width * 1.414)

        converted_points = np.float32([[0,0],[max_width,0],[0,max_height],[max_width,max_height]])

        matrix = cv2.getPerspectiveTransform(input_points,converted_points)
        img_output = cv2.warpPerspective(img_original,matrix,(max_width,max_height))
        cv2.namedWindow("image_output",cv2.WINDOW_NORMAL)
        cv2.imshow("image_output", img_output)

        print(img.shape)
        print(gray.shape)
        print(edged.shape)

    #image stack modification
        gray = np.stack((gray,)*3,axis = -1)
        edged = np.stack((edged,)*3,axis = -1)

        print(img.shape)
        print(gray.shape)
        print(edged.shape)

##        img_hor = np.hstack((img_original,img,gray,edged))
##        cv2.imshow("Contour detection", img_hor)
        cv2.imwrite('D:\\3 rd yr\\cs314_python\\project\\dataset\\bottle_Set\\warped_image.jpeg',img_output)
    #original_resiSize('warped_image.jpeg')
    #readWordz('img_output')

    else:
        x ,y,w,h = cv2.boundingRect(biggest)
        img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,0),2)
        print(img2)
        ROI = img2[y:y+h,x:x+w]
##        cv2.namedWindow('contours',cv2.WINDOW_NORMAL)
##        cv2.imshow('contours',ROI)
        cv2.imwrite('warped_image.jpeg',ROI)
##        print(x)
##        print(y)
##        print(w)
##        print(h)
        print(ROI.shape[0])#w
        print(ROI.shape[1])#h
        input_points = np.float32([[0,0],[ROI.shape[1],0],[0,ROI.shape[0]],[ROI.shape[1],ROI.shape[0]]])

        width = 400
        height = int(width * 1.414)

        converted_points = np.float32([[0,0],[width,0],[0,height],[width,height]])
        matrix = cv2.getPerspectiveTransform(input_points,converted_points)
        img_output = cv2.warpPerspective(ROI,matrix,(width,height))
        cv2.namedWindow("outwar",cv2.WINDOW_NORMAL)
        cv2.imshow("outwar",img_output)
        cv2.waitKey(0)

#This function for reading the images with gray scale
def read_letters_preprosessing(img_):
    pytesseract.pytesseract.tesseract_cmd=r'c:/Program Files/Tesseract-OCR/tesseract.exe'
    print(pytesseract.image_to_string(img_))

    ##Detecting characters
    hImg,wImg = img_.shape
    boxes = pytesseract.image_to_boxes(img_)#x,y,width,height
    for b in boxes.splitlines():
        b = b.split(' ')
        print(b)
        x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
##    #x,y,w(x sould be added),h - noramlly
    # but here correctly giving the vlues ,no need to add
        cv2.rectangle(img_,(x,hImg-y),(w,hImg-h),(0,0,255),3)#color thickneess
    # 1 is the scale,then red color,then thickness as 2
        cv2.putText(img_,b[0],(x,hImg-y+25),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)

    cv2.namedWindow("Result",cv2.WINDOW_NORMAL)
    cv2.imshow("Result",img_)
    cv2.waitKey(0)

def thresholdingGussian(image):
    return cv2.adaptiveThreshold(image,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                 cv2.THRESH_BINARY,21,2)

