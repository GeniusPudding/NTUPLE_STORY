###################################################
# Implement all common UI functions here          #
# "Screen" must be an intance og kivy Screen      #
###################################################
from game_manager import *

#TODO: 按鍵提示語寫法可以更加彈性
def auto_prompt(Screen,press_key,pos_hint,instance, prompt,extra_info=''):#a Screen-bind function
	if prompt:
		print(f'[*] Auto prompt to press {press_key}!')
		Screen.prompt_label = Label(text=extra_info+f'press \'{press_key}\' to continue...',color=(.5,.5,.1,.8),pos_hint=pos_hint,size_hint=(.5,.3),halign='center',valign='center',font_size=84,font_name='res/HuaKangTiFan-CuTi-1.otf')
		Screen.add_widget(Screen.prompt_label)			
		#MUST set remove_widget in Screen's key_action function


def auto_display_speaker(Screen, instance, speaker):#a Screen-bind function
	print('[*] Display speaker: ',speaker)
	Screen.remove_widget(Screen.nametag)
	Screen.canvas.remove_group('speaker')
	if speaker != '':
		source = 'res/images/players/' + speaker + '.png'
		Screen.nametag = Label(text=speaker,pos_hint={'x':0,'y':.2},color=(1,1,1,1),font_size=40,size_hint=(.1,.07),font_name= 'res/HuaKangTiFan-CuTi-1.otf')
		Screen.add_widget(Screen.nametag)
		Screen.canvas.add(Rectangle(source=source,pos=(0,.27*global_h),size=(.15*global_w,.35*global_h),group='speaker'))

class BG_widget(Widget):
	def __init__(self,**kwargs):#, bg_size, bg_pos, bg_source):
		super(BG_widget, self).__init__()
		print(f'init bg, self.parent:{self.parent}')		

	def load_bg(self,bg):
		self.parent.canvas.before.add(bg)
		#self.canvas.before.add(self.bg) #what different?
	def on_touch_down(self, touch): 
		print('bg on_touch_down')
		print(touch)
		print(touch.pos,touch.spos)
class CircleImage(Widget):#Image
	def __init__(self,source, **kargs):
		super(CircleImage, self).__init__( **kargs)
		with self.canvas:
		    self.bg_rect = Ellipse(pos=self.pos,size=self.size,source=source,group='self')
		self.bind(pos=redraw_widget, size=redraw_widget)
		self.source = source

	def start_switching_animate(self,pos,offset,direction,duration=.3):
		(px,py) = pos
		(ox,oy) = offset
		print(f'pos:{pos},offset:{offset},direction:{direction}')
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
		print("anim:",anim)
	def partial_complete_signal(self,instance, widget):
		#print('on_complete')
		if isinstance(self.parent,Screen):
			self.parent.itemframe.playing_anim_num -= 1
			#print('self.parent.itemframe.playing_anim_num:',self.parent.itemframe.playing_anim_num)


def redraw_widget(Widget,*args):
    Widget.bg_rect.size = Widget.size
    Widget.bg_rect.pos = Widget.pos	

freedragging = 0
class FreeDraggableItem(Widget):#for testing allocating mapobjects, and for dragging item
	angle = NumericProperty(0)
	def __init__(self,source,screen=None,magnet=False, **kargs):
		super(FreeDraggableItem, self).__init__( **kargs)
		with self.canvas:
		    self.bg_rect = Ellipse(pos=self.pos,size=self.size,source=source,group='self')
		self.bind(pos=redraw_widget, size=redraw_widget)
		#self.canvas.add(Ellipse(pos=self.pos,size=self.size,source=source,group='self'))
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
		#self.anim.start(se)
	# 	self.anim = Animation(angle = 360, duration=2) 
	# 	self.anim += Animation(angle = 360, duration=2)
	# 	
	def on_touch_down(self, touch):
		print(f"Free item on_touch_down touch.pos:{touch.pos}")
		global freedragging
		if self.collide_point(*touch.pos):
			self.pos = (touch.pos[0]-self.size[0]/2,touch.pos[1]-self.size[1]/2)			 
			freedragging = 1
			self.dragger = 1
			if isinstance(self.screen,Screen): 
				self.screen.item_view = 0 
	def on_touch_move(self, touch):

		if (not self.if_over_boundary(touch.pos)) and self.dragger == 1:#(not self.if_collide_others(touch.pos)) and 		
			self.pos = (touch.pos[0]-self.size[0]/2,touch.pos[1]-self.size[1]/2)

	def on_touch_up(self, touch): #release a dragging item here
		print(f'Free item on_touch_up touch.pos:{touch.pos}"')
		global freedragging 
		freedragging = 0
		self.dragger = 0
		self.stopped_pos_hint = {'x':touch.spos[0],'y':touch.spos[1]}
		self.stopped_pos = touch.pos
		if isinstance(self.screen,Screen) and self.magnet:
			#TODO: 判定解碼是否成功
			screen = self.screen
			if screen.current_mode == 2 and screen.puzzle_pass:#
				print("解碼成功!")
				screen.hp_per_round -= 1
			else:
				self.pos = self.origin_pos
				screen.remove_widget(screen.dragging)
				screen.item_view = 1 #dragging re-added (display_itemframe->auto_focus->auto_focus_item)
				

				
	def start_switching_animate(self,pos,offset,direction,duration=.3):
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


class DraggableItem(Image):#有可能會改成類似FreeDraggableItem的樣子，使其可以拖出道具欄
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
			#print("modified global item_cur_pos:",item_cur_pos) 
		# elif self.dragger == 0:
		# 	self.set_origin_pos()

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
		#print("touch pos,x_radius,y_radius:",touch_pos,x,y)
		for pos in  item_cur_pos[:self.draggable_item_id]+item_cur_pos[self.draggable_item_id+1:]:  #self.other_pos:
			#print("other center:",pos[0]+x,pos[1]+y)
			if (abs(touch_pos[0]-(pos[0]+x)) <= 2*x) and (abs(touch_pos[1]-(pos[1]+y)) <= 2*y):
				#print("touch other's pos:",pos)
				return True
		return False

	# def set_origin_pos(self):
	# 	#TODO: reset this pos when release others
	# 	global dragging
	# 	if dragging == 1 and self.dragger == 0:
	# 		self.pos = self.origin_pos

class SynthesisFrame(Image):#May be deprecated
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
