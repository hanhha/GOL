#!/usr/bin/env python3
import pyglet
from random import getrandbits
from threading import Lock
from argparse import ArgumentParser

import Seenworld as sw

parser = ArgumentParser ()
parser.add_argument ('-wi', '--width', type=int, help = 'width of world in grid cell', default = 64)
parser.add_argument ('-he', '--height', type=int, help = 'height of world in grid cell', default = 64)
parser.add_argument ('-ce', '--cell', type=int, help = 'size of boundary square of a cell', default = 8)
parser.add_argument ('-co', '--continous', help = 'connect sides of 2D grid, left with right and top with bottom', action = 'store_true')
args = parser.parse_args ()

eco_w, eco_h = args.width, args.height 
cell_d = args.cell
cont = args.continous
print ("cont = {0}".format(cont))

sw.circle_radius = cell_d / 2
sw.setup (sw.sep + eco_w*(cell_d + sw.sep), sw.sep + eco_h*(cell_d + sw.sep))

seeds = [[not getrandbits(1) for y in range(eco_h)] for x in range(eco_w)]
world = sw.World (eco_w, eco_h, cell_d, cont, seeds)

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
	if not world.IsHijacked:
		world.GodBearAHandIn ()
	else:
		world.GodLeave ()

def update (dt):
	global generate_lck
	if generate_lck.acquire (False):	
		if not world.IsHijacked:
			world.generate ()
		generate_lck.release ()

pyglet.clock.schedule_interval (update, 0.5)
pyglet.app.run()
# EOF
