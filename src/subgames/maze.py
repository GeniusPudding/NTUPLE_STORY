#from ..subgame_proto import SubGame

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

import numpy as np
import random
import platform
#from PIL import Image as PILImage
import time
import os


cwd = os.getcwd()
OS = platform.system()

print('cwd:',cwd)
res_prefix = ''
if 'subgames' in cwd:
	res_prefix = '../'


maze_blocks_info = np.zeros((20, 20))#0:road, 1:wall

#TODO: solve the directories' level problem and the res path
# try:
# 	f = open('maze.txt','r')#open('res/maze.txt','r')#
# except:
# 	f = open('res/maze.txt','r')
f = open(res_prefix+'res/maze.txt','r')

line_id = 0 
while True:
	line = f.readline()
	#print(walls)
	if len(line) > 0:
		walls = line.strip('\n').split(',')
		for w_id in walls:
			try:
				maze_blocks_info[line_id][int(w_id)] = 1
			except:
				pass
	else:
		break
	line_id += 1

side1 = np.ones((20,2))	
side2 = np.ones((2,24))
extend_maze_blocks_info = np.concatenate((side1,maze_blocks_info,side1),axis=1) 
extend_maze_blocks_info = np.concatenate((side2,extend_maze_blocks_info,side2),axis=0) 

if res_prefix == '../':
	for i in range(len(maze_blocks_info)):
		print([int(block) for block in list(maze_blocks_info[i])])

	for i in range(len(extend_maze_blocks_info)):
		print([int(block) for block in list(extend_maze_blocks_info[i])])

class MazeGame(Screen):# #RelativeLayout):#or inheritant to Screen#SubGame
	cur_pos = (cur_px, cur_py) = init_block = (1,5) #ALL pos_x means vertical axis block id, pos_y means horizontal axis block id in this game
	cur_view = np.zeros((5,5))
	monster1_pos, monster2_pos, monster3_pos= (0,2), (0,11), (7,12)
	target_pos = (7,19)
	def __init__(self, **kwargs):
		super(MazeGame, self).__init__(**kwargs)
		if OS == "Darwin": #Macbook
			import pygame
			self.size = (self.w,self.h) = pygame.display.get_surface().get_size()
		elif OS == "Windows":#at home
			import win32gui
			hwin = win32gui.GetDesktopWindow()
			dt_l, dt_t, dt_r, dt_b = win32gui.GetWindowRect(hwin)
			
			self.size = (self.w,self.h) = (dt_r, dt_b)
   
		#self.ex_px,self.ex_py = self.cur_px+2,self.cur_py+2 #Note the index of extend_maze_blocks_info and maze_blocks_info
		self.cur_view = np.array([row[self.cur_py:self.cur_py+5] for row in extend_maze_blocks_info[self.cur_px:self.cur_px+5]])#np.array(extend_maze_blocks_info[cur_px:cur_px+5])
		# for i in range(len(self.cur_view)):
		# 	print([int(block) for block in list(self.cur_view[i])])

		#self.monsters = [self.monster1_pos,self.monster2_pos,self.monster3_pos] #storeonly values, not references 	 
		#print("init maze")
		

		self.canvas.add(Color( 195/255, 191/255,195/255, .7))
		self.canvas.add(Rectangle(pos=(0,0),size=self.size))
		self.maze_width = int(.8*min(self.w,self.h))
		self.maze_block_len = self.maze_width/5
		self.maze_px, self.maze_py = ((self.w-self.maze_width)/2,(self.h-self.maze_width)/4)
		#print('maze_width:',maze_width)
		#size = (maze_width, maze_width)

		# self.player_img = Image(source='../res/images/testing/maze_player.png',size=(.8*self.maze_block_len,.8*self.maze_block_len),pos=(self.maze_px+2.1*self.maze_block_len,self.maze_py+2.1*self.maze_block_len),size_hint=(None,None))
		# self.add_widget(self.player_img)
		
		self.canvas_draw_blocks()

	def start(self):	
		print('now the subgame start')
		self.keyboard = Window.bind(on_key_down=self.key_action)
		self.e1 = Clock.schedule_interval(self.monster_random_walk, 1)
		self.e2 = Clock.schedule_interval(self.check_collision, .02)	
		self.e3 = Clock.schedule_interval(self.check_arrive_target, .02)
		#super(MazeGame, self).start()#MazeGame, self
	def end(self):
		Clock.unschedule(self.e1)
		Clock.unschedule(self.e2)	
		Clock.unschedule(self.e3)	
		#super(MazeGame, self).end()
		# self.move_view('u')
		# self.move_view('d')
		# self.move_view('d')
		# self.move_view('l')
		# self.move_view('l')
		# self.move_view('r')
		# self.move_view('r')

		#TODO: Try Texture method?
		# texture = Texture.create(size=size)
		# px_size = maze_width*maze_width*3
		# buf = [255]*px_size  #round(x * 255 / px_size) 
		# #for i in range(maze_width*maze_width):  #range(int(.38*min(self.w,self.h))*3,int(.57*min(self.w,self.h))*3):
		# for i in range(maze_width*maze_width*2,px_size):  #range(int(.38*min(self.w,self.h))*3,int(.57*min(self.w,self.h))*3):
		# #for i in range(px_size):  #range(int(.38*min(self.w,self.h))*3,int(.57*min(self.w,self.h))*3):
		# 	if i%3 == 0:
		# 		buf[i] = 255
		# 	elif i%3 == 1:
		# 		buf[i] = 155
		# 	elif i%3 == 2:
		# 		buf[i] = 155
		# #or try pillow or image data
		# im_tex = Image(source='../res/images/testing/wall.png',size=(50,50),size_hint=(None,None)).texture
		# print("im_tex.pixels:",im_tex.pixels)
		# print(f"len(im_tex.pixels):{len(im_tex.pixels)},im_tex.width:{im_tex.width}, im_tex.height:{im_tex.height}")
		# part = im_tex.get_region(0, 0, im_tex.width,2) 
		# print("part.pixels:",part.pixels)
		# print("len(part.pixels):",len(part.pixels))
		# print("part in im_tex:",im_tex.pixels.find(part.pixels))
		# bytes_buf = b''.join([bytes(bc,encoding='utf-8') for bc in [chr(c) for c in buf]] )
		# texture.blit_buffer(bytes_buf, colorfmt='rgb', bufferfmt='ubyte')
		# print("bytes_buf len:",len(bytes_buf))
		# print(f"texture.width:{texture.width}, texture.height:{texture.height}")		
		# # print(f"texture.pixels:{texture.pixels}")
		# #self.canvas.add(Color(1, 1, 1, 1))
		# self.canvas.add(Ellipse(texture=texture, size = size, pos = ((self.w-maze_width)/2,(self.h-maze_width)/4)))


		
	def key_action(self,*args):
		if self.manager.current == 'maze':
			#print('in subgame key: ',*(args))
			if args[1]==276:
				#print ("key action left")
				self.move_view('l')
			elif args[1]==275:
				#print ("key action right")
				self.move_view('r')
			elif args[1]==274:
				#print ("key action down")
				self.move_view('d')
			elif args[1]==273:
				#print ("key action up")
				self.move_view('u')

	def canvas_draw_blocks(self):
		self.canvas.remove_group('blocks')
		#self.remove_widget(self.player_img)
		maze_width = self.maze_width
		maze_block_len = self.maze_block_len
		wall_path = res_prefix+'res/images/testing/wall.png'
		road_path= res_prefix+'res/images/testing/road.png'		
		maze_px, maze_py = self.maze_px, self.maze_py#((self.w-maze_width)/2,(self.h-maze_width)/4)
		#print('maze_px,maze_py,maze_block_len:',maze_px,maze_py,maze_block_len)
		for i,row in enumerate(reversed(range(5))):	
			for col in range(5):
				pos = (maze_px + col*maze_block_len, maze_py + i*maze_block_len)

				if self.cur_view[row][col] == 1: 
					#wall_img = Image(source='../res/images/testing/wall.png',size=(maze_block_len,maze_block_len),size_hint=(None,None))
					wall_img = Rectangle(source=res_prefix+'res/images/testing/wall.png',size=(maze_block_len,maze_block_len),pos=pos,size_hint=(None,None),group = 'blocks')
					self.canvas.add(wall_img)
					#wall_img.pos = pos
					#self.add_widget(wall_img)
				elif self.cur_view[row][col] == 0: 
					#road_img = Image(source='../res/images/testing/road.png',size=(maze_block_len,maze_block_len),pos=pos,size_hint=(None,None))
					road_img = Rectangle(source=res_prefix+'res/images/testing/road.png',size=(maze_block_len,maze_block_len),pos=pos,size_hint=(None,None),group = 'blocks')
					self.canvas.add(road_img)
					#self.add_widget(road_img)	

		# player_img = Rectangle(source='../res/images/testing/maze_player.png',size=(.8*maze_block_len,.8*maze_block_len),pos=(maze_px+2.1*maze_block_len,maze_py+2.1*maze_block_len),size_hint=(None,None))
		# self.canvas.after.add(player_img)
		player_img = Image(source=res_prefix+'res/images/testing/maze_player.png',size=(.8*maze_block_len,.8*maze_block_len),pos=(maze_px+2.1*maze_block_len,maze_py+2.1*maze_block_len),size_hint=(None,None))
		#print(player_img.size)
		self.add_widget(player_img)


	# def on_touch_down(self, touch):
	# 	print(touch.pos)

	def move_view(self,direction):
		#print("direction:",direction)
		moved = 0
		if direction == 'u':
			if self.cur_px > 0 and extend_maze_blocks_info[self.cur_px+1][self.cur_py+2]==0:
				newfound = np.array(extend_maze_blocks_info[self.cur_px-1][self.cur_py:self.cur_py+5]).reshape((1,5))
				self.cur_view = np.concatenate((newfound,self.cur_view[:4]),axis=0)
				self.cur_px -= 1
				moved = 1

		elif direction == 'd':
			if self.cur_px < 23 and extend_maze_blocks_info[self.cur_px+3][self.cur_py+2]==0:
				newfound = np.array(extend_maze_blocks_info[self.cur_px+5][self.cur_py:self.cur_py+5]).reshape((1,5))
				self.cur_view = np.concatenate((self.cur_view[1:],newfound),axis=0)
				self.cur_px += 1
				moved = 1


		elif direction == 'l':
			if self.cur_py > 0 and extend_maze_blocks_info[self.cur_px+2][self.cur_py+1]==0:
				#newfound = np.zeros((5,1))
				newfound = np.array([row[self.cur_py-1] for row in extend_maze_blocks_info[self.cur_px:self.cur_px+5]]).reshape((1,5))
				t_cur_view = self.cur_view.transpose()[:4]
				self.cur_view = np.concatenate((newfound,t_cur_view),axis=0).transpose()
				self.cur_py -= 1
				moved = 1

		elif direction == 'r': 
			if self.cur_py < 23 and extend_maze_blocks_info[self.cur_px+2][self.cur_py+3]==0:
				newfound = np.array([row[self.cur_py+5] for row in extend_maze_blocks_info[self.cur_px:self.cur_px+5]]).reshape((1,5))
				t_cur_view = self.cur_view.transpose()[1:]
				self.cur_view = np.concatenate((t_cur_view,newfound),axis=0).transpose()
				self.cur_py += 1
				moved = 1
		# for i in range(len(self.cur_view)):
		# 	print([int(block) for block in list(self.cur_view[i])])
		self.cur_pos = (self.cur_px, self.cur_py)	

		if moved == 1:
			self.canvas_draw_blocks()

	def reset_game(self):
		self.cur_pos = (self.cur_px, self.cur_py) = self.init_block
		self.cur_view = np.array([row[self.cur_py:self.cur_py+5] for row in extend_maze_blocks_info[self.cur_px:self.cur_px+5]])#np.array(extend_maze_blocks_info[cur_px:cur_px+5])
		self.monster1_pos,self.monster2_pos,self.monster3_pos = (0,2),(0,11),(7,12)
		self.target_pos = (7,19)
		#print("reset self.cur_pos :",self.cur_pos )
		self.canvas.remove_group('monsters')
		self.canvas.remove_group('target')
		self.canvas_draw_blocks()

	def monster_random_walk(self,dt):#):#
		moved_pos = []
		#print("in mrw:",self.monster1_pos,self.monster2_pos,self.monster3_pos)
		for m in [self.monster1_pos,self.monster2_pos,self.monster3_pos]:
			directions = ['u','d','l','r']
			mx,my = m
			if extend_maze_blocks_info[mx+1][my+2]==1:
				directions.remove('u')
			if extend_maze_blocks_info[mx+3][my+2]==1:		
				directions.remove('d')
			if extend_maze_blocks_info[mx+2][my+1]==1:
				directions.remove('l')
			if extend_maze_blocks_info[mx+2][my+3]==1:
				directions.remove('r')
			d = directions[random.randint(0,len(directions)-1)]
			#print('random directions: ',d)
			if d == 'u':
				moved_pos.append((mx-1,my))
			elif d == 'd':
				moved_pos.append((mx+1,my))
			elif d == 'l':
				moved_pos.append((mx,my-1))
			elif d == 'r':
				moved_pos.append((mx,my+1))

		self.monster1_pos = moved_pos[0]
		self.monster2_pos = moved_pos[1]
		self.monster3_pos = moved_pos[2]

		cx, cy = self.cur_px, self.cur_py 
		#print("in mrw, cx, cy:",cx, cy,self.monster1_pos,self.monster2_pos,self.monster3_pos)
		self.canvas.remove_group('monsters')
		for m in [self.monster1_pos,self.monster2_pos,self.monster3_pos]:
			mx,my = m		
			if abs(cx - mx) <= 2 and abs(cy - my) <= 2 :			
				monster_img = Rectangle(source=res_prefix+'res/images/testing/monster.jpg',size=(.6*self.maze_block_len,.6*self.maze_block_len),pos=(self.maze_px+(2+my-cy+.2)*self.maze_block_len,self.maze_py+(2+cx-mx+.2)*self.maze_block_len),size_hint=(None,None),group = 'monsters')
				self.canvas.add(monster_img)			
		#TODO: motion in canvas
		
		#print(f"set monster1_pos:{self.monster1_pos},monster2_pos:{self.monster2_pos},monster3_pos:{self.monster3_pos}")			
				
	def check_collision(self,dt):
		#print("in cc:",self.cur_pos,self.monster1_pos,self.monster2_pos,self.monster3_pos)
		cx, cy = self.cur_px, self.cur_py 
		#print("in cc, cx, cy:",cx, cy)
		self.canvas.remove_group('monsters')
		for m in [self.monster1_pos,self.monster2_pos,self.monster3_pos]:
			mx, my = m
			if abs(cx - mx) <= 2 and abs(cy - my) <= 2 :			
				monster_img = Rectangle(source=res_prefix+'res/images/testing/monster.jpg',size=(.6*self.maze_block_len,.6*self.maze_block_len),pos=(self.maze_px+(2+my-cy+.2)*self.maze_block_len,self.maze_py+(2+cx-mx+.2)*self.maze_block_len),size_hint=(None,None),group = 'monsters')
				self.canvas.add(monster_img)


		if self.cur_pos == self.monster1_pos or self.cur_pos == self.monster2_pos or self.cur_pos == self.monster3_pos:			
			print('collision!')
			popup = Popup(title='遭到魔物襲擊!!',title_size='28sp',title_font=res_prefix+'res/HuaKangTiFan-CuTi-1.otf',title_color=[.2,.9,.1,.9],content=Label(text_size= (400, 400),text='重新開始遊戲......',font_size=64,font_name= res_prefix+'res/HuaKangTiFan-CuTi-1.otf'),size_hint=(None, None), size=(400, 400))
			popup.open()

			self.reset_game()

		# 	return True
		# return False #if schedule_interval callback function return False, then stop scheduling
	def check_arrive_target(self,dt):
		#draw target canvas if in current view
		tx, ty = self.target_pos[0], self.target_pos[1]
		cx, cy = self.cur_px, self.cur_py  
		#print(f'self.cur_pos:{self.cur_pos},self.target_pos:{self.target_pos}')
		self.canvas.remove_group('target')
		if abs(cx - tx) <= 2 and abs(cy - ty) <= 2 :			
			target_img = Rectangle(source=res_prefix+'res/images/testing/mask.jpg',size=(.6*self.maze_block_len,.6*self.maze_block_len),pos=(self.maze_px+(2+ty-cy+.2)*self.maze_block_len,self.maze_py+(2+cx-tx+.2)*self.maze_block_len),size_hint=(None,None),group = 'target')
			self.canvas.add(target_img)

		if self.cur_pos == self.target_pos:			
			print('target!')
			popup = Popup(title='找到女主角!!',title_size='28sp',title_font=res_prefix+'res/HuaKangTiFan-CuTi-1.otf',title_color=[.2,.9,.1,.9],content=Label(text_size=(400, 400),text='於是，又找到了妳',font_size=64,font_name= res_prefix+'res/HuaKangTiFan-CuTi-1.otf'),size_hint=(None, None), size=(400, 400))
			popup.open()

			self.reset_game()
			#TODO: back to screen!!!

class MainApp(App):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.root = MazeGame()
	def build(self):              
		return self.root
if __name__ == '__main__':
	# m = MainApp()
	# m.run()
	MainApp().run()#Why can't execute here
