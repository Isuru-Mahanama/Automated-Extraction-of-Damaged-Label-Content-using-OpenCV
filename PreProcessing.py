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

    cv2.namedWindow("Result",cv2.WINDOW_NORMAL)
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


def read_letters(img_):
    pytesseract.pytesseract.tesseract_cmd=r'c:/Program Files/Tesseract-OCR/tesseract.exe'
    #img_ = cv2.imread(img_path)

    #img_ = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    print(pytesseract.image_to_string(img_))

    ##Detecting characters
    hImg,wImg,channel = img_.shape
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


#read_letters('warped_image.jpeg')
#read_letters('with the box.jpg')
#readWordz('with the box.jpg')


def thresholdingGussian(image):
    return cv2.adaptiveThreshold(image,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                 cv2.THRESH_BINARY,21,2)

def thresholdMean(image):
    return cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                                 cv2.THRESH_BINARY,15,5)

def noiseremoval(image):
    dst = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,15)
    return dst

def skerltonize(img):
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(img,kernel,iterations = 1)
    return erosion

image = 'with the box.jpg'
image_gray = cv2.imread(image,cv2.IMREAD_GRAYSCALE)
image_color = cv2.imread(image,1)
#image_read = cv2.imread(image)



skelton = skerltonize(image_gray)

noise_remove = noiseremoval(image_color)
image_color = cv2.cvtColor(noise_remove,cv2.COLOR_RGB2GRAY)
thresh_guassian = thresholdingGussian(image_color)
#im = cv2.cvtColor(thresh_guassian,cv2.COLOR_GRAY2RGB)


#thresh_mean = thresholdMean(image_gray)


plt.subplot(151)
plt.title('Original Image ')
plt.imshow(image_color)
plt.subplot(152)
plt.title('Grayed Image')
plt.imshow(image_gray,'gray')
plt.subplot(153)
plt.title('Thresholding')
plt.imshow(thresh_guassian,'gray')
plt.subplot(154)
plt.title('Noise Removal')
plt.imshow(noise_remove)
plt.subplot(155)
plt.title('Skelton')
plt.imshow(skelton,'gray')
plt.show()

#read_letters(image_read)
#read_letters(noise_remove)
read_letters_preprosessing(thresh_guassian)
#read_letters_preprosessing(noise_remove)


