###################################################
# Implement all common UI functions here          #
# "Screen" must be an intance og kivy Screen      #
###################################################
from game_manager import *

def auto_prompt(Screen,press_key,pos_hint,instance, prompt,size_hint=(.6,.5),pre_info='',post_info='繼續品味人生...'):#a Screen-bind function
	if prompt:
		print(f'[*] Auto prompt to press {press_key}!')
		Screen.remove_widget(Screen.prompt_label)#for exceptions
		Screen.prompt_label = Label(text=pre_info+f'\n請按\'{press_key}\'鍵\n'+post_info,color=(191/255, 201/255, 202/255, 1),pos_hint=pos_hint,size_hint=size_hint,halign='center',valign='center',font_size=78,font_name='res/HuaKangTiFan-CuTi-1.otf')
		Screen.add_widget(Screen.prompt_label)			
		#MUST set remove_widget in Screen's key_action function

def auto_display_speaker(Screen, instance, name): #a Screen-bind function
	print('[*] Display speaker: ',name)
	Screen.remove_widget(Screen.nametag)
	Screen.canvas.before.remove_group('speaker')
	if name not in ['','N']:
		source = 'res/images/players/' + name + '.png'
		print('displaying speaker source :',source)
		if len(name.split('_')) > 1:
			name = name.split('_')[0]
		Screen.nametag = Label(text=name,pos_hint={'x':0,'y':.2},color=(0,0,0,1),font_size=40,size_hint=(.26,.07),font_name= 'res/HuaKangTiFan-CuTi-1.otf')
		Screen.add_widget(Screen.nametag)
		
		if os.path.isfile(source):
			#Screen.canvas.add(Rectangle(source=source,pos=(0,.27*global_h),size=(.15*global_w,.35*global_h),group='speaker'))
			Screen.canvas.before.add(Rectangle(source=source,pos=(.3*global_w,.05*global_h),size=(.4*global_w,.8*global_h),group='speaker'))

class BG_widget(Widget):
	def __init__(self,**kwargs):#, bg_size, bg_pos, bg_source):
		super(BG_widget, self).__init__()
		print(f'init bg, self.parent:{self.parent}')		

	def load_bg(self,source,*args):
		bg = Rectangle(source=source, pos=(0,0), size=(global_w,global_h),group='bg')
		self.parent.canvas.before.add(bg)

	def on_touch_down(self, touch): #For the flexibility to implement some user interaction functions on the whole screen
		#print('bg on_touch_down')
		print(touch)
		print(touch.pos,touch.spos)

class CircleImage(Widget):#Image
	def __init__(self,source, **kargs):
		super(CircleImage, self).__init__( **kargs)
		self.canvas.clear()
		with self.canvas:
			Color(1,1,1,1)
			self.bg_rect = Ellipse(pos=self.pos,size=self.size,source=source,group='self')
		self.bind(pos=redraw_widget, size=redraw_widget)
		self.source = source

	def start_switching_animate(self,pos,offset,direction,duration=.35):#offset and duration also can be a list, and must have same length 
		(px,py) = pos
		if not isinstance(offset, list):#only a tuple
			(ox,oy) = offset
			
			if direction == 'positive':
				anim = Animation(pos=(px+ox,py+oy), duration=duration)#(x=px+ox, y=py+oy, duration=1)
				anim.bind(on_complete=self.partial_complete_signal)
				anim.start(self)
				self.pos = (px+ox,py+oy) 
			elif direction == 'negative':
				anim = Animation(pos=(px-ox,py-oy), duration=duration )#(x=px-ox, y=py-oy, duration=1)
				anim.bind(on_complete=self.partial_complete_signal)
				anim.start(self)
				self.pos = (px-ox,py-oy)
		else:#Not support directions yet
			if not isinstance(duration, list) or (len(offset)!=len(duration)):
				raise ValueError('Argument \"duration\" must be a list with the same length of \"offset\"')
			else:
				(ox,oy) = offset[0]
				anim = Animation(pos=(px+ox,py+oy), duration=duration[0])
				px += ox
				py += oy 
				for i,of in enumerate(offset[1:]):
					(ox,oy) = of
					anim += Animation(pos=(px+ox,py+oy), duration=duration[i])
					px += ox
					py += oy 
				anim.bind(on_complete=self.partial_complete_signal)
				anim.start(self)
				self.pos = (px,py)
		print(f"After anim... pos:{self.pos}")
	def partial_complete_signal(self,instance, widget):
		#print('on_complete')
		if isinstance(self.parent,Screen):
			self.parent.itemframe.playing_anim_num -= 1
<<<<<<< HEAD
=======


>>>>>>> refs/remotes/origin/master

class ImageButton(ButtonBehavior, Image): #Behavior
	def __init__(self, **kargs):#callback,
		super(ImageButton, self).__init__( **kargs)
		#self.callback = callback
		#self.object_id = object_id#use this if it is an object
	def on_press(self):
		print('ImageButton on_press')
		#self.callback()

def redraw_widget(Widget,*args):
    Widget.bg_rect.size = Widget.size
    Widget.bg_rect.pos = Widget.pos	
def global_free(Widget, free):
	global freedragging
	freedragging = free#為何前後變數id不同

freedragging = 1
class FreeDraggableItem(Widget):#for testing allocating mapobjects, and for dragging item
	free = NumericProperty(1)
	def __init__(self,source,screen=None,magnet=False, **kargs):
		super(FreeDraggableItem, self).__init__( **kargs)
		with self.canvas:
		    self.bg_rect = Ellipse(pos=self.pos,size=self.size,source=source,group='self')
		self.bind(pos=redraw_widget, size=redraw_widget)
		self.bind(free=global_free)

		self.x_radius = self.size[0]/2
		self.y_radius = self.size[1]/2
		self.dragger = 0
		self.stopped_pos_hint = {'x':self.pos[0]/global_w,'y':self.pos[1]/global_h}
		self.origin_pos = self.stopped_pos = self.pos
		self.screen = screen
		self.magnet = magnet
		self.anim = Animation(x=10, y=100, duration=2)
		self.anim.repeat = True
		self.source = source

	def on_touch_down(self, touch):
		print(f"Free item on_touch_down touch.pos:{touch.pos}")
		
		if self.collide_point(*touch.pos):
			self.free = 0
			self.pos = (touch.pos[0]-self.size[0]/2,touch.pos[1]-self.size[1]/2)			
			self.dragger = 1
			if isinstance(self.screen,Screen): 
				self.screen.item_view = 0 #here make focusing_frame_id = -1
	def on_touch_move(self, touch):

		if (not self.if_over_boundary(touch.pos)) and self.dragger == 1:		
			self.pos = (touch.pos[0]-self.size[0]/2,touch.pos[1]-self.size[1]/2)

	def on_touch_up(self, touch): #release a dragging item here
		print(f'Free item on_touch_up touch.pos:{touch.pos}"')
		self.free = 1
		self.dragger = 0
		self.stopped_pos_hint = {'x':touch.spos[0],'y':touch.spos[1]}
		self.stopped_pos = touch.pos
		if isinstance(self.screen,Screen) and self.magnet:
			screen = self.screen
			if screen.current_mode == 1:
				self.reset(screen,1)
			#elif screen.current_mode == 2 and not screen.in_judge_range: 
			# 	#screen.hp_per_round -= 1#DEBUG
				#print('不在判定範圍')
				#screen.judgable = True
				#self.reset(screen,2) #不在判定範圍時直接重置，判定範圍內時需要延遲
	def reset(self,screen,mode,*args):
		#print('reset dragging!')
		self.stopped_pos = self.pos = self.origin_pos
		screen.remove_widget(screen.dragging)	
		#if mode == 1:
		screen.try_open_item_view()# item_view = 1 #dragging re-added (display_itemframe->auto_focus->auto_focus_item),here make focusing_frame_id = cyclic[0]

	def start_switching_animate(self,pos,offset,direction,duration=.2):
		(px,py) = pos
		(ox,oy) = offset
		print(f'pos:{pos},offset:{offset}')
		if direction == 'positive':
			anim = Animation(pos=(px+ox,py+oy), duration=duration )#(x=px+ox, y=py+oy, duration=1)
			anim.start(self)
			self.pos = (px+ox,py+oy) 
		elif direction == 'negative':
			anim = Animation(pos=(px-ox,py-oy), duration=duration )#(x=px-ox, y=py-oy, duration=1)
			anim.start(self)
			self.pos = (px-ox,py-oy)
		print("anim:",anim)

	def if_over_boundary(self, touch_pos):

		if (self.x_radius<=touch_pos[0]) and \
		(touch_pos[0]<=global_w-self.x_radius) and\
		(self.y_radius<=touch_pos[1]) and\
		(touch_pos[1]<=global_h-self.y_radius):
			return False
		return True

def E2_distance(pos1,pos2):
	return math.sqrt(math.pow(pos1[0]-pos2[0],2)+math.pow(pos1[1]-pos2[1],2))	

num_up = {1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:0,0:1}
num_down = {2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8,0:9,1:0}
select_left = {2:1,3:2,0:3,1:0}
select_right = {1:2,2:3,3:0,0:1}
def build_CodedLock(screen,item):
	screen.canvas.add(Color(rgba=(1,1,1,1),group='puzzle')) 
	screen.canvas.add(Rectangle(pos=(.35*global_w,.4*global_h),size=(.3*global_w,.5*global_h),source=item['source'],group='puzzle'))
	screen.cur_code = [1,3,1,4]
	screen.code_id = 0
	code_pos_hint = [{'x':.35+i*.075,'y':.3} for i in range(4)] 	
	screen.code_labels = [Label(color=(.7,.7,.7,.6),text = str(screen.cur_code[i]), size_hint = (.075,.1),pos_hint=code_pos_hint[i],font_size=144 ) for i in range(4)]   
	# screen.code_instructions = Label(color=(1,1,1,1),text = '用方向鍵控制彼此心靈的數字輪盤', size_hint = (.3,.1),pos_hint={'x':.35,'y':.2},font_size=50,font_name='res/HuaKangTiFan-CuTi-1.otf' )
	# screen.add_widget(screen.code_instructions)
	for i in range(4):
		screen.add_widget(screen.code_labels[i])
	select_code_block_canvas(screen, 0)
	screen.item_view = 0
	screen.puzzling = True
def puzzle_move_view(screen, press_key_id):
	if press_key_id == 276:
		screen.code_id = select_left[screen.code_id]
	elif press_key_id == 275:
		screen.code_id = select_right[screen.code_id]
	print('move screen.code_id:',screen.code_id)
	select_code_block_canvas(screen, screen.code_id)

def select_code_block_canvas(screen, code_id):
	screen.canvas.remove_group('block')
	wid = 10
	lb_pos = (global_w*(.35 + code_id*.075), global_h*.3) 
	rb_pos = (global_w*(.35 + (code_id+1)*.075), global_h*.3) 
	rt_pos = (global_w*(.35 + (code_id+1)*.075), global_h*.4) 
	lt_pos = (global_w*(.35 + code_id*.075), global_h*.4) 
	print('lb_pos,rb_pos,rt_pos,lt_pos:',lb_pos,rb_pos,rt_pos,lt_pos)
	screen.canvas.add(Color(.1,.1,.1,.5))
	screen.canvas.add(Line(points=[lb_pos[0], lb_pos[1], rb_pos[0], rb_pos[1], rt_pos[0], rt_pos[1], lt_pos[0], lt_pos[1]],cap=None,joint='round',close=True, width=wid,group='block'))
		
def clear_CodedLock(screen):
	try:
		for i in range(4):
			screen.remove_widget(screen.code_labels[i])
		#screen.remove_widget(screen.code_instructions)
		screen.canvas.remove_group('block')
	except:
		print('No opened Coded Lock')	


def synthesis_canvas(screen,item,stage,*args):
	base_y = .6*global_h
	space_x = .04*global_w
	block_x = .01*global_w
	block_y = .02*global_h
	(bx,by) = block_size = (.12*global_w,.2*global_h)
	block_color = (0,0,0,1)
	box_size = (block_size[0]-2*block_x, block_size[1]-2*block_y)
	box_color = (1,1,1,1)
	operator_color = (.3,1,.2,1)
	operator_x = .1*global_w
	item_len = .8*min(box_size[0],box_size[1])
	item_x, item_y = (box_size[0]-item_len)/2 , (box_size[1]-item_len)/2 
	if stage == 0:#init
		#material
		screen.canvas.add(Color(rgba=block_color,group='synthesis'))
		screen.canvas.add(Rectangle(pos=(space_x,base_y),size=block_size,group='synthesis'))
		screen.canvas.add(Color(rgba=box_color,group='synthesis'))
		screen.canvas.add(Rectangle(pos=(space_x+block_x,base_y+block_y),size=box_size,group='synthesis'))
		screen.canvas.add(Ellipse(source=item['source'],pos=(space_x+block_x+item_x,base_y+block_y+item_y),size=(item_len,item_len),group='synthesis'))
		#'+'
		screen.canvas.add(Color(rgba=operator_color,group='synthesis'))
		screen.canvas.add(Rectangle(pos=(2*space_x+bx,base_y+.07*global_h),size=(operator_x,.06*global_h),group='synthesis'))
		screen.canvas.add(Color(rgba=operator_color,group='synthesis'))
		screen.canvas.add(Rectangle(pos=(2*space_x+bx+.035*global_w,base_y+block_y),size=(.03*global_w,box_size[1]),group='synthesis'))
		#input
		screen.canvas.add(Color(rgba=block_color,group='synthesis'))
		screen.canvas.add(Rectangle(pos=(3*space_x+bx+operator_x,base_y),size=block_size,group='synthesis'))
		screen.canvas.add(Color(rgba=box_color,group='synthesis'))
		screen.canvas.add(Rectangle(pos=(3*space_x+bx+operator_x+block_x,base_y+block_y),size=box_size,group='synthesis'))
		#'='
		screen.canvas.add(Color(rgba=operator_color,group='synthesis'))
		screen.canvas.add(Rectangle(pos=(4*space_x+2*bx+operator_x,base_y+.11*global_h),size=(operator_x,.06*global_h),group='synthesis'))
		screen.canvas.add(Color(rgba=operator_color,group='synthesis'))
		screen.canvas.add(Rectangle(pos=(4*space_x+2*bx+operator_x,base_y+.03*global_h),size=(operator_x,.06*global_h),group='synthesis'))
		#output
		screen.canvas.add(Color(rgba=block_color,group='synthesis'))
		screen.canvas.add(Rectangle(pos=(5*space_x+2*bx+2*operator_x,base_y),size=block_size,group='synthesis'))
		screen.canvas.add(Color(rgba=box_color,group='synthesis'))
		screen.canvas.add(Rectangle(pos=(5*space_x+2*bx+2*operator_x+block_x,base_y+block_y),size=box_size,group='synthesis'))
	elif stage == 1:#wait for synthesis
		screen.canvas.add(Ellipse(source=args[0],pos=(3*space_x+bx+operator_x+block_x+item_x,base_y+block_y+item_y) ,size=(item_len,item_len),group='synthesis1'))
		#magic card
		screen.canvas.add(Rectangle(source='res/images/testing/synthesis.png',pos=(2*space_x+bx+operator_x/2-.125*global_w, base_y-.375*global_h) ,size=(.25*global_w,.45*global_h),group='synthesis1'))

	elif stage == 2:
		screen.canvas.add(Ellipse(source=args[0],pos=(5*space_x+2*bx+2*operator_x+block_x+item_x,base_y+block_y+item_y),size=(item_len,item_len),group='synthesis2'))
	else:
		print(f'synthesis stage {stage} not supported')

#for testing
class DraggableItem(Image):#Deprecated
	def __init__(self, frame_pos, frame_size, draggable_item_id, **kargs):#other_pos
		super(DraggableItem, self).__init__( **kargs)
		# self.size_hint = (None,None)
		# self.source = kargs['source']
		#self.other_pos = other_pos#kargs['other_pos']
		self.frame_pos = frame_pos
		self.frame_size = frame_size
		self.draggable_item_id = draggable_item_id
		#print(f"init item's pos:{self.pos},size:{self.size},source:{self.source},self.parent:{self.parent}")
		#print("global item_cur_pos:",item_cur_pos)
		self.x_radius = self.size[0]/2
		self.y_radius = self.size[1]/2
		self.dragger = 0
		#global item_cur_pos

		print("item_cur_pos id:",id(item_cur_pos),"item_cur_pos :",item_cur_pos)
		#self.origin_pos = item_cur_pos[draggable_item_id]
		#self.canvas.before.add(Ellipse(source=self.source,pos=self.pos,size=self.size))#source=item_tuple[1], #Items grids
			
		#print("dragging:",dragging)
	def on_touch_down(self, touch):
		print(f"item on_touch_down global_x:{global_x},global_y:{global_y}")
		global dragging, item_cur_pos
		if self.collide_point(*touch.pos):
			item_cur_pos[self.draggable_item_id] = self.pos = (touch.pos[0]-self.size[0]/2,touch.pos[1]-self.size[1]/2)			 
			dragging = 1
			self.dragger = 1
			
	def on_touch_move(self, touch):
		# print('item on_touch_move')
		# print(touch.pos,touch.spos)
		global dragging, item_cur_pos 
		if (not self.if_collide_others(touch.pos)) and (not self.if_over_boundary(touch.pos)) and self.dragger == 1:#(dragging == 0 or self.dragger == 1):	#self.scaled_collide_point(touch.pos,2) and 		
			item_cur_pos[self.draggable_item_id] = self.pos = (touch.pos[0]-self.size[0]/2,touch.pos[1]-self.size[1]/2)

	def on_touch_up(self, touch): #release a dragging item here
		# print('item on_touch_up')
		global dragging 
		dragging = 0
		self.dragger = 0

	def if_over_boundary(self, touch_pos):

		if (self.frame_pos[0]+self.x_radius<=touch_pos[0]) and \
		(touch_pos[0]<=self.frame_pos[0]+self.frame_size[0]-self.x_radius) and\
		(self.frame_pos[1]+self.y_radius<=touch_pos[1]) and\
		(touch_pos[1]<=self.frame_pos[1]+self.frame_size[1]-self.y_radius):
			return False
		return True 

	def if_collide_others(self, touch_pos):
		x = self.x_radius
		y = self.y_radius
		global item_cur_pos
		for pos in  item_cur_pos[:self.draggable_item_id]+item_cur_pos[self.draggable_item_id+1:]:  #self.other_pos:
			if (abs(touch_pos[0]-(pos[0]+x)) <= 2*x) and (abs(touch_pos[1]-(pos[1]+y)) <= 2*y):
				#print("touch other's pos:",pos)
				return True
		return False

#for testing
class SynthesisFrame(Image):#Deprecated
	parent_w = NumericProperty()
	parent_h = NumericProperty()
	def __init__(self,rules,**kargs):#parent_w,parent_h,
		super(SynthesisFrame, self).__init__(**kargs)
		self.parent_w = global_w#parent_w
		self.parent_h = global_h#parent_h
		self.synthesis_rules = rules

	def try_synthesis(self):
		#Image as content ?
		self.parent.hp_per_round -= 1
		popup = Popup(title='嘗試鍊成!!',title_size='28sp',title_font='res/HuaKangTiFan-CuTi-1.otf',title_color=[.2,.9,.1,.9],content=Label(text='鍊成中...',font_size=64,font_name= 'res/HuaKangTiFan-CuTi-1.otf'),size_hint=(None, None), size=(400, 400))
		popup.open()

	def on_touch_down(self, touch):  
		x = touch.pos[0]
		y = touch.pos[1]
		print(f'SynthesisFrame on_touch_down x:{global_x},y:{global_y},touch x:{x},touch y:{y},self.pos:{self.pos},self.size:{self.size},self.parent_w:{self.parent_w},self.parent_h:{self.parent_h}')

		if (x>=self.pos[0]) and (y>=(self.pos[1]+self.pos[1]*3/2*.834)) and (y<=self.pos[1]+self.pos[1]*3/2):			
			self.try_synthesis() 
