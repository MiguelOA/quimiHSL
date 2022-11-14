#************************************************************LIBRERIAS
from tkinter import *
from tkinter.filedialog import *
from PIL import ImageTk, Image, ImageGrab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
import cv2
#************************************************************ VARIABLES GLOBALES
# image=""
# canvas=""
# toolbar=""
# myvar=""
# rojo=""
# verde=""
# azul=""
# h=""
# s=""
# l=""
#************************************************************ FUNCIONES PROPIAS

def abrir():
	global image, myvar
	path = askopenfilename(initialdir="Desktop", title='Selecciona imagen', filetype=(("Imagen", ".jpg"), ("All Files", "*.*")))
	im = Image.open(path)
	tkimage = ImageTk.PhotoImage(im.resize((900,500)))
	myvar=Label(frame,image = tkimage)
	myvar.image = tkimage
	image = cv2.imread(path)
	myvar.pack()
	
def calcularHIST_RGB():
	global image, canvas,toolbar, myvar, rojo, verde, azul
	myvar.pack_forget()
	fig=plt.Figure(figsize=(8, 5), dpi=100)
	ax=fig.add_subplot()
	hist_r= cv2.calcHist([image], [2], None, [256], [0, 256])
	hist_g= cv2.calcHist([image], [1], None, [256], [0, 256])
	hist_b= cv2.calcHist([image], [0], None, [256], [0, 256])
	xlim=list(range(0,256))
	ax.plot(xlim, hist_r, "r",xlim, hist_g, "g",xlim, hist_b, "b")
	ax.set_xlabel("Valor RGB")
	ax.set_ylabel("Cuentas")
	canvas = FigureCanvasTkAgg(fig, master=frame)
	toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)
	toolbar.update()
	canvas.draw()
	canvas.get_tk_widget().pack()
	toolbar.pack(side=TOP)
	rojo=np.argmax(hist_r)
	verde=np.argmax(hist_g)
	azul=np.argmax(hist_b)	

def calcularHIST_HLS():
	global rojo, verde, azul, h,s,l, canvas, canvas2, toolbar, myvar
	canvas.get_tk_widget().pack_forget()
	toolbar.pack_forget()
	myvar.pack_forget()

	r = float(rojo)
	g = float(verde)
	b = float(azul)
	r/=255
	g/=255
	b/=255
	M = max(r,g,b)
	m = min(r,g,b)
	d = M-m
	if( d==0 ): 
		h=0
	elif( M==r ): 
		h=((g-b)/d)%6
	elif( M==g ): 
		h=(b-r)/d+2
	else: 
		h=(r-g)/d+4
	h*=60
	if( h<0 ):
		h+=360
	l = (M+m)/2
	if(d==0):
		s = 0
	else:
		s = d/(1-abs(2*l-1))
	s*=100
	l*=100
	fig2, bx = plt.subplots(subplot_kw={'projection': 'polar'})
	bx.plot(h, s, "ro")
	bx.set_rmax(255)
	bx.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
	bx.grid(True)
	bx.set_title("Gráfico polar HS", va='bottom')
	canvas2 = FigureCanvasTkAgg(fig2, master=frame)
	canvas2.draw()
	canvas2.get_tk_widget().place(relx=0.5, rely=0.5, anchor=CENTER)
	GeneTabla()
	
def GeneTabla():
	global h,s,l, frame2
	H=round(h,3)
	S=round(s,3)
	L=round(l,3)
	frame2 = LabelFrame(frame)
	frame2.place(relx=0.7,rely=0.8)
	datos = [['%H', '%S', '%L'],[H,S,L]]
	for tablay, row in enumerate(datos):
		for tablax, item in enumerate(row):
			Tabla = Label(frame2, text=str(item))
			Tabla.grid(row=tablay, column=tablax)

def Borrar():
	for widgets in frame.winfo_children():
		widgets.destroy()	

def saveimagesasPDF():
	fichero = asksaveasfile(title="Guardar", mode='wb',defaultextension=".pdf")
	fichero.write()
	fichero.close()
		
def MostrarImagen():
	global canvas, toolbar, myvar, canvas2, frame2, Tabla
	myvar.pack()
	canvas.get_tk_widget().pack_forget()
	toolbar.pack_forget()
	canvas2.get_tk_widget().place_forget()
	frame2.place_forget()
	for Tabla in frame2.winfo_children():
		Tabla.grid_forget()

def MostrarRGB():
	global canvas, toolbar, myvar, canvas2, frame2, Tabla
	canvas.get_tk_widget().pack()
	toolbar.pack()
	myvar.pack_forget()
	canvas2.get_tk_widget().place_forget()
	frame2.place_forget()
	for Tabla in frame2.winfo_children():
		Tabla.grid_forget()

def MostrarHSL():
	global canvas, canvas2, toolbar, myvar
	canvas2.get_tk_widget().place(relx=0.5, rely=0.5, anchor=CENTER)
	GeneTabla()
	canvas.get_tk_widget().pack_forget()
	toolbar.pack_forget()
	myvar.pack_forget()
	
#************************************************************ VENTANA
window = Tk()
window.title("quimiHS")
window.geometry("1000x700")
window.resizable(False, False)
frame = LabelFrame(window)
frame.place(relx=0.5,rely=0.4, anchor=CENTER)
#-------------------------------------------MENU

menubar = Menu(window)
window.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Abrir",command=abrir)
filemenu.add_command(label="Borrar",command=Borrar)
filemenu.add_command(label="Guardar", command=saveimagesasPDF)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=window.quit)
visualmenu = Menu(menubar, tearoff=0)
visualmenu.add_command(label="Imagen cargada",command=MostrarImagen)
visualmenu.add_command(label="Grafico RGB calculado",command=MostrarRGB)
visualmenu.add_command(label="Grafico HSL",command=MostrarHSL)
menubar.add_cascade(label="Archivo", menu=filemenu)
menubar.add_cascade(label="Visualizacion", menu=visualmenu)

#-------------------------------------------BOTONES
button1 = Button(window, text="Calcular histograma RBG", command=calcularHIST_RGB).place(relx=0.4,rely=0.815,height=40)
button2 = Button(window, text="Calcular HSL", command=calcularHIST_HLS).place(relx=0.6,rely=0.815,height=40)

# def XY():
	# frame.update()
	# print(frame.winfo_x(),frame.winfo_y())
	
button3 = Button(window, text="posiciones", command=XY).place(relx=0.1,rely=0.915,height=40)  
#"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" FINAL

	
window.mainloop()
