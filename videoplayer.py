import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class VideoPlayer:
	def __init__(self):
		window = self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("LazorTouch video")
		window.set_default_size(640, 400)
		window.connect("destroy", gtk.main_quit, "WM destroy")
		vbox = gtk.VBox()
		window.add(vbox)
		self.movie_window = gtk.DrawingArea()
		vbox.add(self.movie_window)
		window.connect("key_press_event", self.on_key_press)
		window.set_events(gtk.gdk.KEY_PRESS_MASK)

		window.show_all()

		self.player = gst.element_factory_make("playbin2", "player")
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)

		self.fullscreen = False
		window.unfullscreen()
	
	def play_video(self, number):
		filepath = os.getcwd() + "/videos/" + str(number)
		if os.path.isfile(filepath):
			self.player.set_state(gst.STATE_READY)
			self.player.set_property("uri", "file://" + filepath)
			self.player.set_state(gst.STATE_PLAYING)
		else:
			print 'Warning: video ' + filepath + " not found."

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

	def on_key_press(self, widget, data=None):
		keyname = gtk.gdk.keyval_name(data.keyval)
		print '.'+str(keyname)+'.'

		if keyname is 'q':
			print 'quit'
			gtk.main_quit()

		if keyname is 'f':
			if self.fullscreen:
				self.window.unfullscreen()
			else:
				self.window.fullscreen()
			self.fullscreen = not self.fullscreen

		if keyname.isdigit():
			print "load video " + keyname
			self.play_video(int(keyname))

