from math import *
import gc
import pyglet
from pyglet.gl import *
import Eco

screen = None
mw, mh, sep = 2,2,1

circle_verts = [0,0]
circle_numpoints = 1

circle_radius = 0
live_color = [0, 255, 0]

def setup (w, h):
	global screen
	global circle_verts
	global circle_numpoints

	for y in range(1, int(circle_radius) + 1):
		x_boundary = sqrt(circle_radius*circle_radius - y*y)
		for x in range (1, int(x_boundary) + 1):
			circle_verts += [ x,  y]
			circle_verts += [-x,  y]
			circle_verts += [ x, -y]
			circle_verts += [-x, -y]
			circle_verts += [ 0,  y]
			circle_verts += [ 0, -y]
			circle_numpoints += 6

	for x in range(1, int(circle_radius) + 1):
		circle_verts += [ x, 0]
		circle_verts += [-x, 0]
		circle_numpoints += 2

	screen = pyglet.window.Window (width = w + 2*mw, height = h + 2*mh, caption = 'Game of Life')

class World:
	def __init__ (self, w, h, cell_d, seeds = None):
		self.w = w
		self.h = h
		self.cell_d = cell_d
		self.width = mw + w*(cell_d + sep) + mw - sep 
		self.height = mh + h*(cell_d + sep) + mw - sep

		self.draw_batch = pyglet.graphics.Batch ()
		self.verts = dict ()

		self.ecosys     = [[Eco.CellEntity (x, y, self.spawn, seeds[x][y] if seeds is not None else False) for y in range (h)] for x in range(w)]
		self.ecosys_pst = [[seeds[x][y] if seeds is not None else False for y in range (h)] for x in range(w)]

	@property
	def EcoSys (self):
		return self.ecosys

	@property
	def EcoState (self):
		return self.ecosys_pst

	def check_neiboughs (self, x, y):
		alive_around = 0
		cands = [[x-1,y-1],[x,y-1],[x+1,y-1],
		         [x-1,y  ],[x+1,y],
		         [x-1,y+1],[x,y+1],[x+1,y+1]]
		for (cand_x,cand_y) in cands:
			if (0 <= cand_x < self.w) and (0 <= cand_y < self.h):
				alive_around += 1 if self.EcoState[cand_x][cand_y] else 0

		return alive_around

	def record (self):
		self.ecosys_pst = [[self.EcoSys[x][y].IsAlive for y in range (0, self.h)] for x in range(0, self.w)]

	def spawn (self, x, y):
		if x not in self.verts:
			self.verts[x] = dict ()
		if y not in self.verts[x]:
			center = [mw + sep + x*(self.cell_d + sep) + circle_radius, mh + sep + y*(self.cell_d + sep) + circle_radius]
			self.verts[x][y] = [circle_verts[i] + center[i % 2] for i in range(len(circle_verts))]

		return self.draw_batch.add (circle_numpoints, GL_POINTS, None, ('v2f', self.verts[x][y]))

	def draw (self):
		glColor3f(live_color[0], live_color[1], live_color[2])
		self.draw_batch.draw ()

	def generate (self):
		for x in range(self.w):
			for y in range(self.h):
				n_alive_neiboughs = self.check_neiboughs (x, y)
				if self.EcoState[x][y]:
					if (n_alive_neiboughs < 2) or (n_alive_neiboughs > 3):
						self.EcoSys[x][y].Die ()
				else:
					if (n_alive_neiboughs == 3):
						self.EcoSys[x][y].Resurrect ()

		#print([[self.EcoSys[x][y].IsAlive for y in range (0, self.h)] for x in range(0, self.w)])
		self.record ()
		#print(self.EcoState)
