#!/usr/bin/env python3
import pyglet
from random import getrandbits
from threading import Lock
import Seenworld as sw

eco_w, eco_h = 64, 64
cell_d = 8 
#eco_w, eco_h = 3, 3
#cell_d = 20

sw.circle_radius = cell_d / 2
sw.setup (sw.sep + eco_w*(cell_d + sw.sep), sw.sep + eco_h*(cell_d + sw.sep))

seeds = [[not getrandbits(1) for y in range(eco_h)] for x in range(eco_w)]
world = sw.World (eco_w, eco_h, cell_d, seeds)

generate_lck = Lock ()

@sw.screen.event
def on_draw ():
	sw.screen.clear ()
	world.draw ()

@sw.screen.event
def on_mouse_release (x, y, button, modifiers):
	global generate_lck

	generate_lck.acquire ()

	cell_x = (x - sw.mw - sw.sep) // (cell_d + sw.sep)	
	cell_y = (y - sw.mw - sw.sep) // (cell_d + sw.sep)	
	if world.EcoState[cell_x][cell_y]:
		world.EcoSys[cell_x][cell_y].Die ()
	else:
		world.EcoSys[cell_x][cell_y].Resurrect ()

	world.EcoState[cell_x][cell_y] = world.EcoSys[cell_x][cell_y].IsAlive

	generate_lck.release ()

@sw.screen.event
def on_key_press (symbol, modifiers):
	print (world.EcoState)

def update (dt):
	global generate_lck
	if generate_lck.acquire (False):	
		world.generate ()
		generate_lck.release ()

pyglet.clock.schedule_interval (update, 0.5)
pyglet.app.run()
# EOF
