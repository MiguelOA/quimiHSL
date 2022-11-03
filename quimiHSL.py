from tkinter import *
from tkinter.filedialog import *
from PIL import ImageTk, Image 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import cv2


window = Tk()
window.title("quimiHS")
window.geometry("500x500")


def abrir():
	path = askopenfilename(initialdir="Desktop", title='Select a File', filetype=(("Imagen", ".jpg"), ("All Files", "*.*")))
	im = Image.open(path)
	tkimage = ImageTk.PhotoImage(im.resize((300,300)))
	myvar=Label(window,image = tkimage)
	myvar.image = tkimage
	myvar.grid(row=25, column=6)
	image = cv2.imread(path)
	
	for i, col in enumerate(['b', 'g', 'r']):
		hist = cv2.calcHist([image], [i], None, [256], [0, 256])
		plt.plot(hist, color = col)
		plt.xlim([0, 256])
	plt.show() 
	
	
button1 = Button(window, text="abrir imagen", command=abrir).grid(row=0, column=0)

window.mainloop()
