#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class VideoPlayer:
	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("LazorTouch video")
		window.set_default_size(500, 400)
		window.connect("destroy", gtk.main_quit, "WM destroy")
		vbox = gtk.VBox()
		window.add(vbox)
		self.movie_window = gtk.DrawingArea()
		vbox.add(self.movie_window)
		window.show_all()
		
		self.player = gst.element_factory_make("playbin2", "player")
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
	
	def play_video(self, number):
		filepath = os.getcwd() + "/" + str(number) + ".mp4"
		if os.path.isfile(filepath):
			self.player.set_property("uri", "file://" + filepath)
			self.player.set_state(gst.STATE_PLAYING)
						
	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
	
	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			gtk.gdk.threads_enter()
			imagesink.set_xwindow_id(self.movie_window.window.xid)
			gtk.gdk.threads_leave()

vplayer = VideoPlayer()
gtk.gdk.threads_init()
vplayer.play_video(2)
gtk.main()

