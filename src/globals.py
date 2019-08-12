# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *#ObjectProperty, StringProperty, NumericProperty, ListProperty, BooleanProperty, ReferenceListProperty
from kivy.graphics import *
from kivy.uix.textinput import TextInput
kivy.resources.resource_add_path('.')
from kivy.graphics.texture import Texture
from kivy.core.window import Window
#from kivy.deps import sdl2, glew
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior,DragBehavior  
from kivy.uix.image import Image
from  kivy.core.image import Image as coreImage
from kivy.animation import Animation

import platform
import sys, datetime
from sys import exit 
import json
import numpy as np
import math
import os
from functools import partial
import random
#from PIL import Image as PILImage
import time

#global constant here
final_chapter = 3#for release: 3
OS = platform.system()
if OS=="Darwin":
	import pygame
elif OS == "Windows":
	import win32gui
global_x = 0
global_y = 0
global_w = 0
global_h = 0

dragging = 0
item_cur_pos = []

def get_screen_size():#TODO: 
	if OS == "Darwin": #Macbook
		w, h = pygame.display.get_surface().get_size()
	elif OS == "Windows":#at home
		
		#TODO: study GetWindowRect
		hwin = win32gui.GetDesktopWindow()
		print('hwin:',hwin)
		dt_l, dt_t, dt_r, dt_b = win32gui.GetWindowRect(hwin)
		print(dt_l, dt_t, dt_r, dt_b )
		from win32api import GetSystemMetrics
		print("Width =", GetSystemMetrics(0))
		print("Height =", GetSystemMetrics(1))
		w, h = (dt_r, dt_b)
	return (w, h)
def global_mouse(*args):
	#global global_x,global_y, 
	global_h = get_screen_size()[1]
	# print('global_x,global_y:',global_x,global_y)
	# print('id(global_x),id(global_y):',id(global_x),id(global_y))
	if OS == "Darwin": #Macbook
		global_x, global_y = pygame.mouse.get_pos()#Bugs in Windows
		global_y = global_h - global_y
	elif OS == "Windows":#at home
		#import pyautogui
		#print("win32gui.GetCursorInfo():",win32gui.GetCursorInfo())
		_,_,(global_x, global_y) = win32gui.GetCursorInfo()
		#global_x, global_y = pyautogui.position()
		global_y = global_h - global_y
	return global_x,global_y
global_w,global_h = get_screen_size()
global_x,global_y = global_mouse()


