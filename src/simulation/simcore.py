"""
SimCore
=======

TODO: Add documentation
"""

from ..common import Log

# Import PyGame
import pygame
from pygame.locals import *

# Import PyOpenGL
import OpenGL
OpenGL.ERROR_CHECKING = True
OpenGL.ERROR_LOGGING = True

from OpenGL.GL import *
from OpenGL.GLU import *

import threading
import time


class SimEngine:
	def __init__(self):
		self.__running = True

	@classmethod
	def __start(self, title, width, height):
		"""
		Create window, initialize simulation and load resources.
		:param title: The title to be displayed on the window border
		:param width: The width that the window will have when created
		:param height: The height that the window will have when created
		"""
		Log.debug("Intializing simulation")

		pygame.init()
		pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

		glViewport(0, 0, width, height)

	@classmethod
	def __update(self, delta):
		"""
		Update the state of the engine.
		:param delta: The time in seconds since the last update occurred
		"""

		pass

	@classmethod
	def __render(self):
		"""
		Render what the camera is seeing onto the window.
		"""
		glClearColor(1.0, 0.0, 0.0, 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		pygame.display.flip()

	@classmethod
	def __handle_event(self, event):
		"""
		Handle events sent by the window.
		:param event: The event to be processed
		"""
		if event.type == pygame.QUIT:
			self.__running = False

	@classmethod
	def __exit(self):
		"""
		Perform all necessary cleanup before terminating the simulation.
		"""
		Log.debug("Exiting simulation");
		pygame.quit()

	@classmethod
	def run(self, title, width, height, framerate):
		"""
		Execute the core engine loop. Initialization, updating, rendering, event handling
		and termination are managed by the engine loop.
		:param title: The title to be displayed on the window border
		:param width: The width that the window will have when created
		:param height: The height that the window will have when created
		"param framerate: The maximum number of frames per second allowed
		"""
		self.__start(title, width, height)

		time_millis = lambda: int(round(time.time() * 1000))
		frame_time = 1.0 / framerate * 1000.0
		frame_count = 0

		last_time = time_millis()
		last_render_time = time_millis()
		last_tick_time = time_millis()

		self.__running = True
		while self.__running:
			# Handle events
			for event in pygame.event.get():
				self.__handle_event(event)

			elapsed_time = time_millis() - last_time
			last_time = time_millis()

			# Update
			self.__update(elapsed_time / 1000.0)

			# Render
			if (time_millis() - last_render_time) >= frame_time:
				last_render_time = time_millis()
				frame_count += 1

				self.__render()
			else:
				time.sleep(0.001)

			# This is executed once a second
			if (time_millis() - last_tick_time) >= 1000:
				last_tick_time = time_millis()
				frame_count = 0

		self.__exit()

def init():
	def core():
		sim = SimEngine()
		sim.run("ROV Simulation", 1280, 720, 60)

	thread = threading.Thread(target=core, args=())
	thread.start()