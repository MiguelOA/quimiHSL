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
	
	fig=plt.Figure(figsize=(5, 4), dpi=100)
	ax=fig.add_subplot()
	hist_r= cv2.calcHist([image], [2], None, [256], [0, 256])
	hist_g= cv2.calcHist([image], [1], None, [256], [0, 256])
	hist_b= cv2.calcHist([image], [0], None, [256], [0, 256])
	xlim=list(range(0,256))
	ax.plot(xlim, hist_r, "r",xlim, hist_g, "g",xlim, hist_b, "b")
	ax.set_xlabel("Valor RGB")
	ax.set_ylabel("Cuentas")
	canvas = FigureCanvasTkAgg(fig, master=window)
	canvas.draw()
	canvas.get_tk_widget().grid(row=25, column=16)
	
	
button1 = Button(window, text="abrir imagen", command=abrir).grid(row=0, column=0)

window.mainloop()
