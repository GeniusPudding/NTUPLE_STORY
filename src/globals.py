# -*- coding: utf-8 -*-
###################################################
# For all import packages                         #
###################################################
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
from kivy.core.image import Image as coreImage
from kivy.animation import Animation
from kivy.input.motionevent import MotionEvent
from kivy.core.audio import SoundLoader
from kivy.utils import escape_markup

import platform
import sys, datetime
from sys import exit 
import json
import numpy as np
import math
import os
os.environ['KIVY_AUDIO'] = 'sdl2'
from functools import partial
import random
#from PIL import Image as PILImage
import time
import pickle
import shutil
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

def get_screen_size(): 
	if OS == "Darwin": #Macbook
		w, h = pygame.display.get_surface().get_size()
	elif OS == "Windows":#Win10
		hwin = win32gui.GetDesktopWindow()
		#print('hwin:',hwin)
		dt_l, dt_t, dt_r, dt_b = win32gui.GetWindowRect(hwin)
		#print(dt_l, dt_t, dt_r, dt_b )
		from win32api import GetSystemMetrics
		#print("Width =", GetSystemMetrics(0))
		#print("Height =", GetSystemMetrics(1))
		w, h = (dt_r, dt_b)
	return (w, h)


global_w,global_h = get_screen_size()



