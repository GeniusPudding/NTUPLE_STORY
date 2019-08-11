import kivy
kivy.require('1.10.0')
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.app import App
import kivy
from kivy.graphics import *
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.properties import *
import platform
import os

cwd = os.getcwd()
res_prefix = ''
if 'subgames' in cwd:#TODO: solve windows problem
	res_prefix = '../'


#print("cwd,res_prefix:",cwd,res_prefix)
global_w, global_h = 0,0
OS = platform.system()	
if OS == "Darwin": #Macbook
	import pygame
	global_w, global_h = pygame.display.get_surface().get_size()
elif OS == "Windows":#at home
	import win32gui
	hwin = win32gui.GetDesktopWindow()
	dt_l, dt_t, dt_r, dt_b = win32gui.GetWindowRect(hwin)
	global_w, global_h = dt_r, dt_b
   
class PuzzleGame(Screen):
	def __init__(self, **kwargs):
		super(PuzzleGame, self).__init__(**kwargs)
		self.continuous_tasks = [Permutation(name='perm'), CodedLock(name='coded') , ColorCodedLock(name='colorcoded') ]
		self.cur_task_id = 0


	def start(self):

		self.keyboard=Window.bind(on_key_down=self.key_action)
		
		print("subgame start") 
		for task in self.continuous_tasks:
			self.manager.add_widgets(task)
		self.manager.current = 'perm'
	def reset_game(self):
		print("subgame reset") 

	def end(self):
		print("subgame end") 	

class Permutation(Screen):
	def __init__(self, **kwargs):
		super(Permutation, self).__init__(**kwargs)

		self.add_widget(Button(text='next task',on_press=self.next_task) )
	def next_task(self, btn):
		self.manager.current = 'coded'
num_up = {1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:0,0:1}
num_down = {2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8,0:9,1:0}
select_left = {2:1,3:2,0:3,1:0}
select_right = {1:2,2:3,3:0,0:1}
class CodedLock(Screen):
	cur_select_id = NumericProperty(-1)
	cur_view = ListProperty([-1]*4)
	def __init__(self, **kwargs):
		super(CodedLock, self).__init__(**kwargs)
		self.add_widget(Button(background_color = (.2,.2,.3,.7),text='next task',on_press=self.next_task, pos_hint={'x':.2,'y':.1},size_hint=(.15,.15)) )
		global global_w, global_h 
		self.size = (global_w, global_h )
		self.canvas.add(Color(.8,1,.3,.5))
		self.canvas.add(Rectangle(pos=self.pos,size=self.size))

		self.canvas.add(Color(1,1,0,.5))
		self.canvas.add(Rectangle(pos=(global_w*.25,global_h*.35),size=(global_w*.5,global_h*.35)))
		#self.canvas.add(Line(points=[100, 100, 200, 100, 100, 200], width=10))
		for i in range(4):
			self.canvas.add(Color(1,1,1,.9))
			self.canvas.add(Rectangle(pos=(global_w*(.27 + i*.12) ,global_h*.375),size=(global_w*.1,global_h*.3)))			

		self.password = [5,4,8,7]#background_color = (1,0,0,1),
		#self.numbers = [Label(text = str(i), size_hint = (.1,.3),pos_hint={'x':.27,'y':.375}, font_size = 184) for i in range(10)]
		self.current_numbers = []
		self.bind(cur_select_id=self.auto_generate_select_block)
		self.bind(cur_view=self.auto_display_numbers)
		self.keyboard=Window.bind(on_key_down=self.key_action)
		self.cur_select_id = 0
		self.cur_view = [0,0,0,0]
				
	def auto_display_numbers(self, ins, val):
		print('auto_display_numbers')
		for nLabel in self.current_numbers:
			self.remove_widget(nLabel)
		for i,num in enumerate(val):
			l = Label(color=(0,0,1,1),text = str(num), size_hint = (.1,.3),pos_hint={'x':.27+ i*.12,'y':.375},font_size=184 )#self.numbers[num]
			#l.pos_hint['x'] = .27 + i*.12
			self.current_numbers.append(l)
			self.add_widget(l)

	def auto_generate_select_block(self, ins, val):
		#global global_w,global_h
		self.canvas.remove_group('block')
		#pos=(global_w*(.27 + i*.12) ,global_h*.375),size=(global_w*.1,global_h*.3)
		i = val
		wid = 10
		print("auto_generate_select_block, self.size:",self.size)
		lb_pos = (global_w*(.27 + i*.12), global_h*.375) 
		rb_pos = (global_w*(.37 + i*.12), global_h*.375) 
		rt_pos = (global_w*(.37 + i*.12), global_h*.675) 
		lt_pos = (global_w*(.27 + i*.12), global_h*.675) 
		self.canvas.add(Color(0,1,1,1))
		self.canvas.add(Line(points=[lb_pos[0], lb_pos[1], rb_pos[0], rb_pos[1], rt_pos[0], rt_pos[1], lt_pos[0], lt_pos[1]],cap=None,joint='round',close=True, width=wid,group='block'))

	def next_task(self, btn):
		self.manager.current = 'colorcoded'

	def key_action(self,*args):
		#if self.manager.current == 'coded':
		if args[1]==276:
			self.move_view('l')
		elif args[1]==275:
			self.move_view('r')
		elif args[1]==274:
			self.select_number('d')
		elif args[1]==273:
			self.select_number('u')
	def move_view(self, direction):

		#control part:
		if direction == 'l':
			self.cur_select_id = select_left[self.cur_select_id]
		elif direction == 'r':
			self.cur_select_id = select_right[self.cur_select_id]
		print('move self.cur_select_id:',self.cur_select_id)

		#canvas part:		

	def select_number(self, direction):

		#control part:
		if direction == 'u':
			self.cur_view[self.cur_select_id] = num_up[self.cur_view[self.cur_select_id]]
		elif direction == 'd':
			self.cur_view[self.cur_select_id] = num_down[self.cur_view[self.cur_select_id]]
		print(f'select self.cur_view[{self.cur_select_id}]:{self.cur_view[self.cur_select_id]}')

		#canvas part:
		if self.cur_view == self.password:
			popup = Popup(title='正確答案!!',title_size='28sp',title_font=res_prefix+'res/HuaKangTiFan-CuTi-1.otf',title_color=[.2,.9,.1,.9],content=Label(text_size= (400, 400),text='密碼:5487',font_size=64,font_name= res_prefix+'res/HuaKangTiFan-CuTi-1.otf'),size_hint=(None, None), size=(400, 400))
			popup.open()

class ColorCodedLock(Screen):
	def __init__(self, **kwargs):
		super(ColorCodedLock, self).__init__(**kwargs)

		self.add_widget(Button(text='back to story',on_press=self.back_to_story))

	def back_to_story(self):
		self.manager.current = 'story'

class MainApp(App):
	def __init__(self,test_id , **kwargs):
		super().__init__(**kwargs)
		self.root = [Permutation(name='perm'), CodedLock(name='coded') , ColorCodedLock(name='colorcoded') ][test_id]
	def build(self):              
		return self.root
if __name__ == '__main__':
	# m = MainApp()
	# m.run()

	MainApp(test_id=1).run()#Why can't execute here