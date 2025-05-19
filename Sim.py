import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import matplotlib.patches



''' Define constants'''

Nx = 40
Ny = 40

dt = 0.05
alpha_0 = 1.17


T = np.zeros((Ny, Nx))



T[:, 0] = 0.0
T[:, -1] = 0.0
T[0, :] = -10.0
T[-1, :] = 0.0
T[0, :] = 0.0

alpha_to_color = {1.65 : '#C0C0C0', 0.0035 : '#D7C4A3', 0.88 : '#708090'}



''' Define Material and Heat source classes '''

def sorted_C(coor):
	c_x = sum(c[0] for c in coor) / len(coor)
	c_y = sum(c[1] for c in coor) / len(coor)
	def angle(P):
		return (math.atan2(P[1] - c_y, P[0] - c_x))
	return (sorted(coor, key=angle))

def Polygon(N_x, N_y, coor, alpha):
	sorted_coor = sorted_C(coor)

	inside_points = np.zeros((N_y, N_x))
	for x in range(0, N_x):
		for y in range(0, N_y):
			inside = False
			for i in range(len(coor)):
				x1, y1 = sorted_coor[i]
				x2, y2 = sorted_coor[(i+1) % len(coor)]
				if ((y1 > y) != (y2 > y)):
					try:
						x_inter = (x2 - x1) * (y - y1) / (y2 - y1) + x1
						if x < x_inter:
							inside = not inside
					except:
						if x < x1:
							inside = not inside
			if inside:
				inside_points[x, y] = alpha - alpha_0
	return (inside_points)



class Material:
	instances = []


	def __init__(self, coor, alpha):
		self.coor = coor
		self.alpha = alpha
		self.polygon = Polygon(Nx, Ny, coor, alpha)
		Material.instances.append(self)


class HeatSource:
	instances = []


	def __init__(self, x, y, rate):
		self.x = x
		self.y = y
		self.rate = rate
		HeatSource.instances.append(self)
		T[y, x] += rate



'''
iron = Material([(3, 15), (2, 2), (11, 15)], 0.3)
HeatSource(20, 10, 7)
HeatSource(3, 10, 7)
HeatSource(35, 18, 4)
'''



''' Update Function'''

def HeatUpdate(T):
	alpha = np.ones((Ny, Nx)) * 1.17 + sum(a.polygon for a in Material.instances)
	dx = 1.0 / Nx
	dy = 1.0 / Ny
	laplace = (np.roll(T, -1, axis=0) + np.roll(T, 1, axis=0) - 2 * T)
	laplace += (np.roll(T, -1, axis=1) + np.roll(T, 1, axis=1) - 2 * T)
	T_new = T + alpha * dt * laplace
	for hs in HeatSource.instances:
		T_new[hs.y, hs.x] += hs.rate
	T_new[0, :] = 0.0
	T_new[-1, :] = 0.0
	T_new[:, 0] = 0.0
	T_new[:, -1] = 0.0
	T_new -= np.ones((Ny, Nx)) * 30 / (Nx * Ny)
	return T_new

'''
print (T.shape)
for i in range(1, 1000):
	T = HeatUpdate(T)
'''

def Simulate():
	fig, ax = plt.subplots()
	im = plt.imshow(T, cmap='coolwarm', interpolation='bicubic')

	for new_material in Material.instances:
		SC = sorted_C(new_material.coor)
		SC_order = []
		for a in SC:
			SC_order += [(a[1], a[0])]
		SC = SC_order
		polygon = matplotlib.patches.Polygon(SC, closed=True, facecolor=alpha_to_color[new_material.alpha], edgecolor=alpha_to_color[new_material.alpha], alpha=0.3)
		ax.add_patch(polygon)

	T_new = T

	def update(frame):
		im.set_array(HeatUpdate(im.get_array()))

	ani = animation.FuncAnimation(fig, update, frames = 100, interval=40, blit=False)
	plt.show()
