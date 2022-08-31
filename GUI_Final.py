import tkinter as tk
from tkinter import *
import os
from PIL import Image,ImageTk
import tkinter.font as font
from tkinter.filedialog import askopenfile
from warp_connected_with_GUI import *

root = tk.Tk()
root.geometry('+%d+%d'%(125,10))

# heder area
header = Frame(root,width = 800, height = 175 , bg = "white")
header.grid(columnspan = 3 , rowspan = 2, row = 0)

# content
canvas = tk.Canvas(root, height = 650, width = 1100, bg = "#191970")
canvas.grid(columnspan = 3,rowspan = 2 , row =0)

frame = tk.Frame(root , bg="#F0FFFF")
frame.place(relwidth = 0.8 ,relheight = 0.8 , relx = 0.1,rely = 0.1 )
# Logo
logo = Image.open('Logo4.jpeg')
logo = logo.resize((300,300))
logo = ImageTk.PhotoImage(logo)
logo_Label = tk.Label(image = logo)
logo_Label.image = logo
logo_Label.grid(column = 3,row = 0 and 1)


#Logo 2
logo = Image.open('lo.png')
logo = logo.resize((550,150))
logo = ImageTk.PhotoImage(logo)
logo_Label = tk.Label(image = logo)
logo_Label.image = logo
logo_Label.grid(column = 1,row = 0)


#Instruction
instruction = tk.Label(root, text = "Select the Bottle Image on your PC to extract its label!!!!!!!", fg = "white" ,bg ="#800000",font = ("Raleway",15) )
instruction.grid(column = 1 ,row = 2)

def openfile():
    browse_text.set("loading ...")
    file = askopenfile(parent = root,mode = 'rb',title = "Choose a image",filetype=[("all files", (".png",".jpeg",".jpg"))])
    if file:
        name = os.path.basename(file.name)
        warping(name)


browse_text = tk.StringVar()
#letter = tkFont.Font(family="Helvetica", size=12, weight=tkFont.BOLD,slant=tkFont.ITALIC)
#print(letter)
f = font.Font(weight="bold")
browse_btn = tk.Button(root, textvariable = browse_text , font =("Raleway",50),command = lambda:openfile(),fg = "#1A0000", bg ="#FFB3B3",height = 4,width = 20)
browse_btn['font'] = f
browse_text.set("Select Your Image")
browse_btn.grid(column = 1,row =1)

canvas = tk.Canvas(root, height = 300, width = 1100, bg = "#1A0000")
canvas.grid(columnspan = 3)

root.mainloop()

