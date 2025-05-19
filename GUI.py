import tkinter as tk
import tkinter.font as font
from tkinter import filedialog

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Polygon

import numpy as np

import Sim


# Define Simulator functions and Values

chosen_points = []
red_dots = []

Nx = 40
Ny = 40

clean_data = np.zeros((Nx, Ny))



dt = 0.5
alpha_0 = 1.17


T = np.zeros((Ny, Nx))



T[:, 0] = 0.0
T[:, -1] = 0.0
T[0, :] = -10.0
T[-1, :] = 0.0

materials = ['Silver', 'Rubber', 'Silicon']
material_alpha = {'Silver' : 1.65, 'Rubber': 0.0035, 'Silicon': 0.88}
alpha_to_color = {1.65 : '#C0C0C0', 0.0035 : '#D7C4A3', 0.88 : '#708090'}


def CreateHeatSource():
	print ('Creating heat source...')
	rate = HSrate.get()
	global chosen_points
	for i in chosen_points:
		Sim.HeatSource(i[1], i[0], float(rate) * 10)
	chosen_points = []
	print ('Heat source created')

def CreateMaterial():
	print ('Defining Material...')
	alpha_new = selected_mat.get()
	alpha_new = material_alpha[alpha_new]
	global chosen_points
	new_material = Sim.Material(chosen_points, alpha_new)
	number_of_points = len(chosen_points)
	chosen_points = []
	global clean_data
	clean_data += new_material.polygon

	SC = Sim.sorted_C(new_material.coor)
	SC_order = []
	for a in SC:
		SC_order += [(a[1], a[0])]
	SC = SC_order

	polygon = Polygon(SC, closed=True, facecolor=alpha_to_color[new_material.alpha], edgecolor=alpha_to_color[new_material.alpha], alpha=1)
	ax.add_patch(polygon)
	''' Remove Red Dots '''
	global red_dots
	for i in range(len(red_dots) - number_of_points, len(red_dots)):
		red_dots[i].remove()
	canvas.draw()
	print ('Material Defined')



'''
	SC = Sim.sorted_C(new_material.coor)
	SC += [SC[0]]
	for i in range(0, len(SC) - 1):
		ax.plot([SC[i][1], SC[i+1][1]], [SC[i][0], SC[i+1][0]], color=alpha_to_color[new_material.alpha], linewidth=2)


'''

''' Base GUI '''

bg_main = '#121212'
bg_second = '#1E1E1E'
active_color = '#212121'
text_color = '#AB47BC'


root = tk.Tk()
root.title("Simulator GUI")
root.configure(bg=bg_main)
root.geometry("1500x1000")

big_font = font.Font(family='Halvetica', size=20)
small_font = font.Font(family='Halvetica', size=10)
title = tk.Label(root, text="Heat Simulator", bg=bg_main, fg=text_color, font=big_font)
title.pack()



''' Matplot Graph'''

def on_click(event):
	if event.inaxes:
		x, y = int(event.xdata), int(event.ydata)
		print (x, y)
		global chosen_points
		chosen_points += [(y, x)]
		global red_dots
		dot, = ax.plot(x, y, 'ro')
		red_dots += [dot]
		canvas.draw()

fig = Figure(figsize=(4, 4), dpi=100)


fig.patch.set_facecolor(bg_main)
ax = fig.add_subplot(111)

''' coloring '''
axes_color = 'white'
ax.tick_params(color=axes_color)

ax.imshow(clean_data, cmap='grey_r', interpolation='bilinear')


canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

canvas.mpl_connect('button_press_event', on_click)

''' Heat Source '''

HS = tk.Frame(root)
HS.configure(bg=bg_main)
HS.pack(pady=25)


CreateHS = tk.Button(HS, text="Create heat source", bg=bg_second, activebackground=active_color, fg=text_color, bd=0, command=CreateHeatSource)
CreateHS.pack(side='left', padx=30)

HSrateText = tk.Label(HS, text="Heat rate [K/s]:", bg=bg_main, fg=text_color, font=small_font)
HSrateText.pack(side='left')


HSrate = tk.Entry(HS, width=5, bd=0, fg=text_color, bg=bg_second)
HSrate.insert(0, '1')
HSrate.pack(side='left', padx=5)




''' Material '''

Mat = tk.Frame(root)
Mat.configure(bg=bg_main)
Mat.pack()


CreateMat = tk.Button(Mat, text="Insert different material component", activebackground=active_color, bg=bg_second, fg=text_color, bd=0, command=CreateMaterial)
CreateMat.pack(side='left', padx=30)

CMtext = tk.Label(Mat, text="Material: ", bg=bg_main, fg=text_color, font=small_font)
CMtext.pack(side='left')



selected_mat = tk.StringVar(value=materials[0])

Cmat = tk.OptionMenu(Mat, selected_mat,  *materials)
Cmat.config(bg=bg_second, fg=text_color, activebackground=active_color, bd=0)
Cmat['menu'].config(bg=bg_second, fg=text_color, activebackground=active_color, bd=0)

Cmat.pack(side='left')


# Simulate button
Op = tk.Frame(root)
Op.configure(bg=bg_main)
Op.pack()

Simulate = tk.Button(Op, text="Simulate", bg=bg_second, activebackground=active_color, fg=text_color, bd=0, command=Sim.Simulate)
Simulate.pack(side='left', pady=50)

# Run the GUI
def Run_GUI():
	root.mainloop()
