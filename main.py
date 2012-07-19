#!/usr/bin/env python

import sys, os
import gtk, gobject
from videoplayer import VideoPlayer
from laser_stub import Laser


# main logic lives here
class LazorTouch:
	def __init__(self):
		self.laser_ready = False
		self.vplayer = VideoPlayer()
		self.laser = Laser()
		self.buttons = None
		self.oldbuttons = None
# poll interval in msec. 40 would be good in use, 1000 when testing
		gobject.timeout_add(1000, self.poll_laser)

	def poll_laser(self):
		if not self.laser_ready:
			self.laser_ready = self.laser.is_ready()
#			print 'poll - laser not ready'
			return True
		self.oldbuttons = self.buttons
		self.buttons = self.laser.scan()
		if(self.oldbuttons is None):
			self.oldbuttons = self.buttons
#		print 'poll - buttons: ' + str(self.buttons)
		for i in range(len(self.buttons)):
#			print 'idx ' + str(i) + " is " + str(self.buttons[i]) + " was " + str(self.oldbuttons[i])
			if self.oldbuttons[i] is 0 and self.buttons[i] is 1:
				self.button_pressed(i)
		return True

	def button_pressed(self, number):
		print 'button ' + str(number) + " pressed!"
		self.vplayer.play_video(number)

#start main class
lazortouch = LazorTouch()
#and gtk stuff
gtk.gdk.threads_init()
gtk.main()

