

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import imutils


def readWordz(img_path):
    pytesseract.pytesseract.tesseract_cmd=r'c:/Program Files/Tesseract-OCR/tesseract.exe'
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray,11,17,17)#Noise Reduction
    edged = cv2.Canny(bfilter,30,200)#Edge detection
    img_ =cv2.cvtColor(edged,cv2.COLOR_BGR2RGB)


#img_ = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
##Detecting characters
    hImg,wImg,channel = img_.shape
    boxes = pytesseract.image_to_data(img_)#x,y,width,height
    print(boxes)
#print(boxes)
    for x,b in enumerate(boxes.splitlines()):
        if x!=0:        #first line is  heading(first raw)
            b = b.split()
            print(b)
        if len(b) == 12:
             x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
####    #x,y,w(x sou ld be added),h - noramlly
##    # but here correctly giving the vlues ,no need to add
             cv2.rectangle(img_,(x,y),(w+x,h+y),(0,0,255),3)#color thickneess
##    1 is the scale,then red color,then thickness as 2
             cv2.putText(img_,b[11],(x,hImg),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)

    cv2.imshow("Result",img_)
    cv2.waitKey(0)


def original_resiSize(img_path):
    dpi = 80
    im_data = plt.imread(img_path)
    height,width,depth = im_data.shape

    #size of the image need to be
    figsize = width/float(dpi),height/float(dpi)

    #create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize = figsize)
    ax = fig.add_axes([0,0,1,1])

    ax.axis('off')
    ax.imshow(im_data,cmap = 'gray')
    plt.show()


def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1500:#1500
            peri = cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i,0.015*peri,True)
            if area > max_area and len(approx) <= 15:
                biggest = approx
                max_area = area
    return biggest

        #6
img = cv2.imread('IMG-20220812-WA0012.jpg',1)
img1 = img.copy()
print(img.shape[0])#512#1000
print(img.shape[1])#384#572
if(img.shape[0] > 1000):
   img = imutils.resize(img, width=500 )#500
    
if(img.shape[0] > img.shape[1]):
    if(img.shape[0] < 700 and img.shape[0] > 350):
        img = cv2.resize(img,(430,530))#400,500#430,530
    else:
        img = cv2.resize(img,(400,500))
        
img_original = img.copy()
#laplaciian
#img = cv2.Laplacian(img,cv2.CV_8U,ksize = 3)
# Image modification
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray',gray)
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

cv2.imshow('Image with countours',img)


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

    cv2.namedWindow("main",cv2.WINDOW_NORMAL)
    img_hor = np.hstack((img_original,img,gray,edged))
    cv2.imshow("main", img_hor)
    cv2.imwrite('D:\\3 rd yr\\cs314_python\\project\\dataset\\bottle_Set\\warped_image.jpeg',img_output)
#original_resiSize('warped_image.jpeg')
#readWordz('img_output')

else:
    
    mask = np.zeros(img.shape,np.uint8)
    mask.fill(0)
    ct = cv2.drawContours(mask,[biggest],-1,(255,0,255),2)
    cv2.imshow('contours',ct)
    out = cv2.fillConvexPoly(mask,biggest,(255,255,255))
    cv2.namedWindow("out",cv2.WINDOW_NORMAL)
    output = cv2.bitwise_and(img,out)
    cv2.imshow("out",output)
    #####
##    result = cv2.matchTemplate(img1,output,cv2.TM_CCOEFF)
##    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
##    top_left = max_loc
##
##   
##    height,width,channels = img.shape
##    
##
##    bottom_right = (top_left[0] + width ,top_left[1]+height)
##    output2 = output.copy()
##    cv2.rectangle(output2,top_left,bottom_right,255,10)
    cv2.imwrite('with the box.jpg',output)
    
    




    cv2.waitKey(0)



