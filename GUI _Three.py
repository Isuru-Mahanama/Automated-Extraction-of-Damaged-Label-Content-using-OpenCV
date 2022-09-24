import tkinter as tk
from tkinter import *
import os
from PIL import Image,ImageTk,ImageOps
import tkinter.font as font
from tkinter.filedialog import askopenfile
from warp_connected_with_GUI import *

root = Tk()
root.geometry('+%d+%d'%(50,10))

header = Frame(root, width=1200, height=220, bg="white")
header.grid(columnspan=3, rowspan=2, row=0)

img_menu = Frame(root, width=1200, height=20)
img_menu.grid(columnspan=3, rowspan=1, row=2)


main_content = Frame(root, width=1200, height=450, bg="#20bebe")
main_content.grid(columnspan=3, rowspan=2, row=4)

logo_Label_original = Label(root)
logo_Label =Label(root)
text_box = Text(root)
def open_file():
      
      browse_text.set("loading...")
      file = askopenfile(parent=root, mode='rb', filetypes=[("all files", (".png",".jpeg",".jpg"))])

      if file:
        file2 = 1
        name = os.path.basename(file.name)
        extracted_Image = warping(name)
        
        letters = read_letters_preprosessing(extracted_Image)
        display_textbox(letters)
        logo = Image.open(name)
        logo = resize_image(logo)
        
        logo = ImageTk.PhotoImage(logo)
        global logo_Label_original
        logo_Label_original.destroy()
        logo_Label_original = tk.Label(image = logo)

        logo_Label_original.image = logo
        logo_Label_original.grid(column = 0,row = 4 ,sticky=W, padx=100, pady=25)
       


        logo1 = Image.open('warped_image.jpeg')
        logo1 = resize_image(logo1)
        logo1 = ImageTk.PhotoImage(logo1)
        global logo_Label
        logo_Label.destroy()
        logo_Label = tk.Label(image = logo1)
        logo_Label.image = logo1
        logo_Label.grid(column = 1,row = 4,sticky=W,pady=25)


def display_textbox(content):
    global text_box
    text_box.destroy()
    text_box = Text(root, height=20, width=30, padx=10, pady=10)
    text_box.insert(1.0, content)
    text_box.tag_configure("center", justify="center")
    text_box.tag_add("center", 1.0, "end")
    text_box.grid(column=2, row=4, sticky=W,  pady=25)
    browse_text.set("Browse")

def delete_image(logolabel,logo_Label_original,text_box):
    logolabel.destroy()
    logo_Label_original.destroy()
    text_box.destroy()
    browse_btn['state'] =NORMAL


    

        
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


instructions = Label(root, text="Select an Image", font=("Raleway", 15), bg="white")
instructions.grid(column=2, row=0, sticky=N, padx=75, pady=70)

browse_text = StringVar()

browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font=("Raleway",12), bg="#20bebe", fg="white", height=1, width=15)

browse_btn2 = Button(root,text='Delete_image',command=lambda:delete_image(logo_Label,logo_Label_original,text_box),font=("Raleway",12), bg="#20bebe", fg="white", height=1, width=15)  
browse_text.set("Browse")
browse_btn.grid(column=2, row=0, sticky=S, padx=50)
browse_btn2.grid(column=2, row=1, sticky=N, padx=50)
