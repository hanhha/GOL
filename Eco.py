#!/usr/bin/env python3

class Cell (object):
	def __init__ (self):
		self.alive = False

	@property
	def IsAlive (self):
		return self.alive

	def Die (self):
		self.alive = False

	def Resurrect (self):
		self.alive = True

class CellEntity (Cell):
	def __init__ (self, x, y, spawn_func, alive = False):
		Cell.__init__ (self)
		self.x = x
		self.y = y
		self.spawn_func = spawn_func
		if alive:
			self.Resurrect ()
			self.entity = self.spawn_func (self.x, self.y)
		else:
			self.entity = None 

	def Die (self):
		#print ("x %d y %d is killed"%(self.x, self.y))
		Cell.Die (self)
		self.entity.delete ()

	def Resurrect(self):
		#print ("x %d y %d is born"%(self.x, self.y))
		Cell.Resurrect (self)
		self.entity = self.spawn_func (self.x, self.y)

# EOF
