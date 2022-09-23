import tkinter as tk
from tkinter import *
import os
from PIL import Image,ImageTk,ImageOps
import tkinter.font as font
from tkinter.filedialog import askopenfile
from warp_connected_with_GUI import *

root = Tk()
root.geometry('+%d+%d'%(50,10))
#header area - logo & browse button
header = Frame(root, width=1200, height=220, bg="white")
header.grid(columnspan=3, rowspan=2, row=0)

img_menu = Frame(root, width=1200, height=30)
img_menu.grid(columnspan=3, rowspan=1, row=2)

what_img = Label(root,text = "Image 1 of 5",font =("shanti",10))
what_img.grid(row =2 ,column =1)

save_IMG = Frame(root, width=1200, height=50, bg="#C8C8C8")
save_IMG.grid(columnspan=3, rowspan=1, row=3)

#main content area - text and image extraction
main_content = Frame(root, width=1200, height=400, bg="#20bebe")
main_content.grid(columnspan=3, rowspan=2, row=4)


def open_file():
      
      browse_text.set("loading...")
      file = askopenfile(parent=root, mode='rb', filetypes=[("all files", (".png",".jpeg",".jpg"))])

      if file:
        file2 = 1
        name = os.path.basename(file.name)
        extracted_Image = warping(name)
        #display_images(extracted_Image)
        letters = read_letters_preprosessing(extracted_Image)
        display_textbox(letters)
        logo = Image.open(name)
        logo = resize_image(logo)
        #logo = logo.resize((100,150))
        logo = ImageTk.PhotoImage(logo)
        logo_Label = tk.Label(image = logo)
##        if LogoLabel_pre != null:
##              logo_Label.destroy()
        logo_Label.image = logo
        logo_Label.grid(column = 0,row = 4 ,sticky=W, padx=100, pady=25)


##      #########################3
        #extracted_Image = resize_image(extracted_Image)
        #logo = logo.resize((100,150))
        #name = os.path.basename('warped_image.jpeg')
##        name = os.path.basename('warped_image.jpeg')
##        logo = Image.open(name)
##        logo = resize_image(logo)
##        logo1 = ImageTk.PhotoImage(logo)
##        logo_Label = tk.Label(image = logo1)
##        logo_Label.image = logo
##        logo_Label.grid(column = 1,row = 4, pady=25)

        ##########################
        logo1 = Image.open('warped_image.jpeg')
        logo1 = resize_image(logo1)
        logo1 = ImageTk.PhotoImage(logo1)
        logo_Label = tk.Label(image = logo1)
        logo_Label.image = logo1
        logo_Label.grid(column = 1,row = 4,sticky=W,pady=25)



##def display_images(img):
##      
##      
##
##      img = Image.fromarray(np.ones((100, 100, 3), dtype=np.uint8))  # RGB image
##      img = ImageOps.invert(img)
##      cv2.imshow('n',img)
##      base = Image.getmodebase(img.mode)
##      if img.mode != base:
##            img = image.convert(base)
##            img = resize_image(img)
##            mode = Image.getmodebase(mode)
##            img = ImageTk.PhotoImage(mode)
##            img_label= Label(image=img, bg="white")
##            img_label.image = img
##            img_label.grid(row=4, column=1)
##            return img_label
def display_textbox(content):
    text_box = Text(root, height=20, width=30, padx=10, pady=10)
    text_box.insert(1.0, content)
    text_box.tag_configure("center", justify="center")
    text_box.tag_add("center", 1.0, "end")
    text_box.grid(column=2, row=4, sticky=W,  pady=25)

def delete_image(logolabel):
    logolabel.destroy()
##    image_2=Label(root,image=img2)
##    image_2.place(x=0,y=0)

    

        
def resize_image(img):
    width, height = int(img.size[0]), int(img.size[1])
    if width > height:
        height = int(450/width*height)
        #width = 300
        width = 450
    elif height > width:
        width = int(350/height*width)
        height = 350
    else:
        width, height = 350,350
    img = img.resize((width, height))
    return img

def display_logo(logo,x,y):
    logo = Image.open(logo)
    logo = logo.resize((450,150))
    logo = ImageTk.PhotoImage(logo)
    logo_Label = tk.Label(image = logo)
    logo_Label.image = logo
    logo_Label.grid(column = 0,row = 0)


display_logo("LOGOH.png",0,0)


instructions = Label(root, text="Select a PDF file", font=("Raleway", 10), bg="white")
instructions.grid(column=2, row=0, sticky=SE, padx=75, pady=5)

#browse button
browse_text = StringVar()
browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font=("Raleway",12), bg="#20bebe", fg="white", height=1, width=15)
browse_btn2 = Button(root,text='Delete_image',command=lambda:delete_image(logo_Label)).place(x=200,y=200)  
browse_text.set("Browse")
browse_btn.grid(column=2, row=0, sticky=NE, padx=50)
browse_btn2.grid(column=2, row=1, sticky=NE, padx=50)
