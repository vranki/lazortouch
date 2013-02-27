#!/usr/bin/env python

import pygame
from pygame.locals import *
from math import *
import time
import copy
import dbus
import sys

# you will need python 2.x and pygame 

import sick_interface2
reload(sick_interface2)

import sick_dummy
reload(sick_dummy)

import user_interface
reload(user_interface)


def world2pix(pt, scale, x_offset, y_offset):
    return [int(pt[0] * scale + x_offset), int(pt[1] * scale + y_offset)]

def cartesian(pt):
    y = pt[1]/10*cos(pt[0]*pi/180)
    x = pt[1]/10*sin(pt[0]*pi/180)
    return (x,y)

def draw_box(screen, box, scale, x_offset, y_offset):
    pos = world2pix([box[0], box[1]], scale, x_offset, y_offset)
    size = world2pix([box[2]-box[0], box[3]-box[1]], scale, 0, 0)
    pygame.draw.rect(screen, (0,0,0), [pos[0], pos[1], size[0], size[1]], 2)
    #print "box", pos, size

def draw_laser_data(screen, laser_meas, scale, x_offset, y_offset):
    for pt in laser_meas:
        pt_pos_cm = cartesian(pt)
        pt_pos_pix = world2pix(pt_pos_cm, scale, x_offset, y_offset)
        pygame.draw.circle(screen, (0,0,255), pt_pos_pix, 2)

def draw_circles(screen, circles, pressed, scale, x_offset, y_offset):
    for i in range(len(circles)):
        pos = circles[i][0:2]
        circ_pos_pix = world2pix(pos, scale, x_offset, y_offset)
        circ_rad1 = int(circles[i][2]*scale)
        circ_rad2 = int(circles[i][3]*scale)

        if pressed[i]:
            pygame.draw.circle(screen, (20,20,20), circ_pos_pix, circ_rad1, 0)
        else:
            pygame.draw.circle(screen, (20,20,20), circ_pos_pix, circ_rad1, 1)

        pygame.draw.circle(screen, (20,20,20), circ_pos_pix, circ_rad2, 1) 
        
        

#########################################################################
## main
#########################################################################

if len(sys.argv) > 1 and sys.argv[1] == "-nographics":
    graphics = False
else:
    graphics = True


pygame.init()
x_size_pix = 1000
y_size_pix = 700

if graphics:
    screen = pygame.display.set_mode((x_size_pix, y_size_pix))
    screen.fill((250,250,250))

x_offset = x_size_pix/2
y_offset = 0
scale = 1

clock = pygame.time.Clock()

print "Starting..."

my_laser = sick_interface2.SICK()

print "Laser initialized"

ui = user_interface.User_interface("conf.ini")

print "Configuration read"

bus = dbus.SessionBus()
remote_object = bus.get_object("org.hs5w.VideoPlayer","/player")
#iface = dbus.Interface(remote_object, "org.hs5w.VideoPlayer")

print "IPC up and running"

bounding_box = ui.get_bounding_box()
circles = ui.get_circles()

my_laser.start_measurement()
status = 0
#while status < 7:
#    status = my_laser.measurement_status()
#    time.sleep(1)

print "Laser ready for measuring"

old_time = time.time()

old_activation = "None"

running = True
while running:

    for ev in pygame.event.get():
        if ev.type == QUIT:
            running = False
            break

    mouse_pos_pix = pygame.mouse.get_pos()
    mouse_pos_cm = (mouse_pos_pix[0]/scale - x_offset, mouse_pos_pix[1]/scale - y_offset)

    time.sleep(0.05)

    got_data, laser_meas = my_laser.scan_once()

    if not got_data:
        continue

    pressed, activation = ui.update(laser_meas, mouse_pos_cm)
    #print "p", pressed, activation

    if old_activation != activation:
#        iface.PlayFile(activation)
        remote_object.playFile(int(activation))
        print "change video to", activation
        old_activation = activation

    if graphics:
        screen.fill((250,250,250))

        draw_box(screen, bounding_box, scale, x_offset, y_offset)
        draw_circles(screen, circles, pressed, scale, x_offset, y_offset)
        draw_laser_data(screen, laser_meas, scale, x_offset, y_offset) 

        pygame.draw.circle(screen, (0,0,255), mouse_pos_pix, 2)     
    
        pygame.display.flip()

my_laser.close_connection()
pygame.quit()
    

    



