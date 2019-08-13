###################################################
# Main screen of this game                        #
###################################################
from game_manager import *

GM = GameManagerScreen()


class ItemFrame(FloatLayout):
	parent_w = NumericProperty()
	parent_h = NumericProperty()
	focusing_frame_id = NumericProperty(-1)
	item_list = ListProperty([])
	#offset = ListProperty((0,0))
	switchable = BooleanProperty(True)
	playing_anim_num = NumericProperty()
	def __init__(self,**kwargs):
		super(ItemFrame, self).__init__(**kwargs)
		print(f"init itemframe global_w:{global_w},global_h:{global_h},self.size:{self.size},self.parent={self.parent}:")

		self.parent_w = global_w#parent_w
		self.parent_h = global_h#parent_h
		self.infoFrame = Widget()
		self.item_name = Widget()
		self.infoContent = Widget()

		self.bind(item_list=self.auto_gen_items)
		self.bind(focusing_frame_id=self.auto_focus)

		# print("self.x,self.y:",self.x,self.y)
		self.front_pos = (.75*global_w,.4*global_h)
		self.back_pos = (.85*global_w,.45*global_h)#for animations

		self.offset = (0,0)
		self.count = 0
		self.item_size = (.04*global_w,.06*global_h)
		self.info_size_x, self.info_size_y = .12*global_w,.18*global_h


	def auto_gen_items(self,instance,item_list):#focusing_frame_id must be self.cyclic[0] when first open the frame after modified item_list
		print('[*]item frame gen items:',item_list)
		self.count = len(item_list)
		print("item_list:",item_list)
		self.offset = (.1/(self.count-1)*global_w,.05/(self.count-1)*global_h)
		for i in range(self.count):
			print('test append pos')
			item_cur_pos.append([(.75*global_w + i*self.offset[0]),(.4*global_h+i*self.offset[1])])
		print('GM.object_table:',GM.object_table)
		d_len = min(.15*global_w,.2*global_h)
	
		for object_id in item_list:
			print('source:',GM.object_table[str(object_id)]['source'])
		self.item_images =  [CircleImage(pos=item_cur_pos[i],size_hint=(None,None),size=(d_len,d_len) ,source=GM.object_table[str(object_id)]['source']) for i,object_id in enumerate(item_list)] 
		#item_images與item_list共用focusing_frame_id, 另開一個循環id用來展示選取動畫
		#when item_images modified, manually modified the item_list
		self.cyclic = {}
		for i in range(self.count):
			self.cyclic[i] = i


	#dynamic generate part:	
	def auto_focus(self, instance, focusing_frame_id):#handle the info and object id
		print('auto focus frame id:',focusing_frame_id)
		print('current self.item_list:',self.item_list)
		screen = self.parent
		object_id = self.item_list[focusing_frame_id]
		#clear the last status
		for event in screen.dialog_events:
			event.cancel()	
		clear_dialogframe_text(screen,screen.displaying_character_labels)		
		if focusing_frame_id >=0 :	
			self.display_item_info(object_id,screen)
			self.display_item_name(object_id,screen)
			screen.focusing_object_id = object_id
		else:
			screen.remove_widget(self.item_name)
			screen.focusing_object_id = -1

	#TODO: add the select circle
	# def generate_select_block(self,focusing_frame_id):
	# 	self.canvas.remove_group('block')
	# 	i = focusing_frame_id
	# 	wid = 5
	# 	lb_pos = (global_w*(self.pos_hint['x']+.0075 + .0475*(i%3)), global_h*(self.pos_hint['y'] +.02+.08*(i//3))) 
	# 	rb_pos = (global_w*(self.pos_hint['x']+.0075 + .0475*(i%3)+.04), global_h*(self.pos_hint['y'] +.02+.08*(i//3))) 
	# 	rt_pos = (global_w*(self.pos_hint['x']+.0075 + .0475*(i%3)+.04), global_h*(self.pos_hint['y'] +.02+.08*(i//3)+.06))  
	# 	lt_pos = (global_w*(self.pos_hint['x']+.0075 + .0475*(i%3)), global_h*(self.pos_hint['y'] +.02+.08*(i//3)+.06))
	# 	self.canvas.add(Color(0,1,1,1))
	# 	self.canvas.add(Line(points=[lb_pos[0], lb_pos[1], rb_pos[0], rb_pos[1], rt_pos[0], rt_pos[1], lt_pos[0], lt_pos[1]],cap='none',joint='bevel',close=True, width=wid,group='block'))


	def display_item_name(self,object_id,screen):
		screen.remove_widget(self.item_name)
		self.item_name = Label(text= GM.object_table[str(object_id)]['name'],pos_hint={'x':0,'y':.2},color=(.7,1,.4,1),font_size=40,size_hint=(.1,.07),font_name= 'res/HuaKangTiFan-CuTi-1.otf')
		screen.add_widget(self.item_name)
	def display_item_info(self,object_id,screen):
		print('auto_display_item_info object_id:',object_id)
		text_line = GM.object_table[str(object_id)]['description']
		spent_time = line_display_scheduler(screen,'',text_line,False,.2,.5,.15, chars_of_row = 15,rows = 3)
		Clock.schedule_once(partial(clear_dialogframe_text,screen,screen.displaying_character_labels),.05+spent_time)

			
	def switching_frame_focus(self,screen,press_key_id):#handle the cyclic animation
		self.switchable = False
		self.playing_anim_num = self.count #determined by the number of animations
		n = self.count
		d_len = min(.15*global_w,.2*global_h)

		# for i in range(n):
		# 	print(f'self.item_images[{i}].pos:{self.item_images[self.cyclic[i]].pos}')

		if press_key_id==276:
			print ("key action left")
	

			#store last pos:	
			final_pos = self.front_pos
			init_pos = self.back_pos
			#print('final_pos:',final_pos,'init_pos:',init_pos)
			self.curve_animation(screen,self.item_images[self.cyclic[n-1]],init_pos,final_pos)
			for i in range(n-1):
				im = self.item_images[self.cyclic[i]]
				im.start_switching_animate(im.pos,self.offset,'positive')

			#redraw for the correctness of overlapped order	and update the cyclic indice
			for i in reversed(range(n)):
				self.cyclic[i] -= 1
				self.cyclic[i] %= n
				#print(f'redraw self.item_images[{self.cyclic[i]}].pos:{self.item_images[self.cyclic[i]].pos}')
				screen.remove_widget(self.item_images[self.cyclic[i]])
				screen.add_widget(self.item_images[self.cyclic[i]])	

			#By definition, cyclic[0] = focusing_frame_id
			if self.focusing_frame_id <= 0:
				self.focusing_frame_id = n - 1
			else:
				self.focusing_frame_id -= 1	

		elif press_key_id==275:#TODO:complete the animation here
			print ("key action right")


			#store last pos:	
			final_pos = self.back_pos
			init_pos = self.front_pos
			#print('final_pos:',final_pos,'init_pos:',init_pos)
			self.curve_animation(screen,self.item_images[self.cyclic[0]],init_pos,final_pos)
			for i in range(1,n):
				im = self.item_images[self.cyclic[i]]
				im.start_switching_animate(im.pos,self.offset,'negative')

			#redraw for the correctness of overlapped order	and update the cyclic indice
			for i in reversed(range(n)):
				self.cyclic[i] += 1
				self.cyclic[i] %= n
				#print(f'redraw self.item_images[{self.cyclic[i]}].pos:{self.item_images[self.cyclic[i]].pos}')
				screen.remove_widget(self.item_images[self.cyclic[i]])
				screen.add_widget(self.item_images[self.cyclic[i]])

			#By definition, cyclic[0] = focusing_frame_id	
			if self.focusing_frame_id >= n - 1:
				self.focusing_frame_id = 0
			else:
				self.focusing_frame_id += 1				


		print('self.cyclic:',self.cyclic,'self.playing_anim_num:',self.playing_anim_num)

		self.switchable = True


	def curve_animation(self,screen,animatable_im,init_pos,final_pos):#TODO: 逼近半圓曲線
		ix,iy = init_pos
		fx,fy = final_pos
		(mx,my) = middle_pos = ((ix+fx)/2 + abs((iy-fy)/2), (iy+fy)/2 - abs((ix-fx)/2))
		print('middle_pos:',middle_pos)
		offset_1 = (mx-ix,my-iy)
		offset_2 = (fx-mx,fy-my)
		if fy > iy:
			# animatable_im.start_switching_animate(animatable_im.pos,offset_1,'positive',duration=.6)
			# animatable_im.start_switching_animate(animatable_im.pos,offset_2,'positive',duration=.4)
			animatable_im.start_switching_animate(animatable_im.pos,[offset_1,offset_2],None,duration=[.6,.4])
		else:
			# animatable_im.start_switching_animate(animatable_im.pos,offset_1,'positive',duration=.4)	
			# animatable_im.start_switching_animate(animatable_im.pos,offset_2,'positive',duration=.6)
			animatable_im.start_switching_animate(animatable_im.pos,[offset_1,offset_2],None,duration=[.4,.6])

	def use_item(self,screen,object_id,touch=None,*args):#the entry of using items in itemframe, behave samely as click on the focusing item
		print("use item args:",args)#self.parent.current_mode == 1 here
		item = GM.object_table[str(object_id)]	
		types = item['function_types']
		# if touch is None:#TODO: controlable MotionEvent
		# 	touch = MotionEvent(device=None,id='mouse2',profile=['pos'],is_touch=True)#,)

		if len(types) == 1:#'item' only, 
			
			if touch is not None:
				print("拿起一般道具!")
				screen.add_widget(screen.dragging)
				screen.dragging.on_touch_down(touch)
				print(f'use_item freedragging:{freedragging},id(freedragging):{id(freedragging)}')
			else:
				print("普通道具，無法單獨使用!")#TODO:display

		else :#type:trigger, lock, puzzle, synthesis 原則上剩一種
			if screen.current_mode == 1:
				if 'trigger' in types:
					print('觸發劇情!進入劇情模式!')#TODO:display
					screen.current_mode = 3
					return
				behavior_type = types.remove('item')[0]
				screen.enter_puzzle_mode(object_id, behavior_type)		

			elif screen.current_mode == 2:
				if touch is not None:
					print("拿起道具!")
					screen.add_widget(screen.dragging)
					screen.dragging.on_touch_down(touch)
					print(f'use_item freedragging:{freedragging},id(freedragging):{id(freedragging)}')
	def on_touch_down(self, touch):
		#for testing
		print('itemframe touch.profile:',touch.profile,'touch.id:',touch.id,'touch.pos:',touch.pos)
		if self.parent is not None and self.focusing_frame_id >= 0 and self.item_images[self.focusing_frame_id].collide_point(*touch.pos):
			object_id = self.item_list[self.focusing_frame_id]
			screen = self.parent
			self.use_item(screen,object_id,touch)




class StoryScreen(Screen):#TODO: 如何扣掉Windows電腦中screen size的上下面, 注意image檔案拉扯問題
	#TODO: EXCEPTIONS!!!
	#TODO: 釐清property之必要性 有些可以bind function
	
	current_player_id = NumericProperty()
	current_chapter = NumericProperty(-1)
	current_player_chapter = ReferenceListProperty(current_player_id, current_chapter)
	current_map = NumericProperty(-1)
	chapter_maps = ListProperty()
	current_speaker_name = StringProperty()
	hp_per_round = NumericProperty(-1)
	w = NumericProperty(100)
	h = NumericProperty(100) 
	button_width = NumericProperty(0.15)
	dialogframe_width = NumericProperty(0.85)	
	dialogframe_height = NumericProperty(0.2)
	button_height = NumericProperty(0.125) 
	bg_height = NumericProperty(0.8)
	item_list = ListProperty([])
	#dropdown = ObjectProperty(DropDown())
	end_round = BooleanProperty(False)
	complete_chapter = BooleanProperty(False)
	bg_widget = ObjectProperty(Widget())
	itemframe = ObjectProperty(Widget())
	dialog_view = NumericProperty(0)#0:background view(exploring maps), 1:dialog view
	item_view = NumericProperty(0)#0:background view(exploring maps), 1:item view
	chapter_info = ObjectProperty()#rebind=True
	seal_on = BooleanProperty(False)
	current_mode = NumericProperty(-1)#0:precursor mode, 1:exploring mode, 2: puzzle mode, 3:plot mode
	finish_auto = BooleanProperty(False)
	nametag = ObjectProperty(Label())
	dialog_events = ListProperty()
	reload_item_list = BooleanProperty(False)
	focusing_object_id = NumericProperty(-1)
	dragging = ObjectProperty(FreeDraggableItem(source=''))
	puzzle_pass = BooleanProperty(False)
	current_scene = StringProperty('')
	#initialize of the whole game, with fixed properties and resources
	def __init__(self, **kwargs):
		super(StoryScreen, self).__init__(**kwargs)
	def start_story(self,linked_GM):
		global GM
		GM = linked_GM

		self.size = (self.w,self.h) = (global_w,global_h)#get_screen_size()#default size is (100,100)
		print(f"global_w:{global_w},global_h:{global_h}")	
		self.button_height = self.dialogframe_height/2
		print("init pos={},size={},self={},type(self)={},(w,h)={},Window.size={}".format(self.pos,self.size,self,type(self),(self.w,self.h),Window.size))
		self.bind(hp_per_round=self.auto_hp_canvas)
		self.bind(current_speaker_name=partial(auto_display_speaker,self))
		self.bind(current_map=self.auto_switch_maps)
		self.bind(current_player_chapter=self.auto_reload_chapter_info)
		self.bind(chapter_info=self.auto_load_chapter_info_contents)
		self.bind(dialog_view=self.auto_dialog_view)
		self.bind(item_view=self.auto_item_view)
		self.bind(complete_chapter=self.auto_new_chapter)
		self.bind(seal_on=self.auto_seal)
		self.bind(current_mode=self.auto_switch_mode)
		self.bind(finish_auto=partial(auto_prompt,self,'Enter',{'x':.25,'y':.4}))
		self.bind(reload_item_list=self.auto_reload_item_list)
		self.bind(focusing_object_id=self.auto_focus_item)
		Window.bind(on_key_down=self.key_action)
		Window.bind(on_key_up=self.key_release)
		self.hp_widgets = []
		self.displaying_character_labels = []
		#self.nametag = Label()#(Image(),Label())
		sub_size = max(self.w*self.button_width*.6,self.h*self.button_height*.8)
		self.subgame_button = ImageButton(callback=self.to_game_screen,source='res/images/testing/subgame_icon.png',pos_hint={'x':self.dialogframe_width+self.button_width-sub_size/self.w,'y':self.dialogframe_height},size_hint=(sub_size/self.w,sub_size/self.h))


		self.bg_widget = BG_widget(parent =self)
		self.add_widget(self.bg_widget) #bg_size=(self.w,self.h*.75),bg_pos=(0,self.h*.25),bg_source=self.get_screen_path()))

		self.load_game() #auto load/save this game, or set a button

	#the entry of main function in each round 	
	def next_round(self,*args):
		print("Enter function: next_round")
		#<clear the last round status>: 清除前一位玩家回合狀態 	
		self.end_round = False#TODO: if true, 出現輪下一位玩家的按鈕或按鍵提示
		self.complete_chapter = False
		#for testing
		self.remove_widget(self.subgame_button)

		#<modify game info>: 配置回合切換所需 
		self.current_player_id, self.current_chapter = GM.change_turn()#bind function: auto_load_chapter_info_contents
		print("player:{}, chapter:{} ,self.size:{}".format(self.current_player_id, self.current_chapter,self.size))		
		
		#round-binding canvas: 
		self.hp_per_round = 5#trigger event

		#generate personal item list
		#self.generate_item_tag()

		#<chapter info part>: 透過bind auto_load_chapter_info_contents，從 chapter_info 載入所有地圖所需
		self.current_map = -1
		self.current_map = 0#trigger the map loading function
		print("self.chapter_maps[self.current_map]:",self.chapter_maps[self.current_map])

		#for testing, load subgame button 
		self.add_widget(self.subgame_button)

		#for testing
		self.testing_objects_path_init()

		#for testing
		self.add_widget(MapObject(screen=self, object_id=88,object_content=GM.object_table[str(88)],touch_range='default',size_hint=(.2,.2),pos_hint={'x':.3,'y':.3}))

		#auto save
		self.save_game()



	def auto_switch_mode(self, instance, mode):#Entry of all stroy screen modes
		print('[*]Switch mode:', mode)
		if mode == 0:#For each chapter starts
			self.dialog_view = 1#auto_dialog_view	
			self.finish_auto = False
			auto_play_dialog(self,self.auto_dialog)

		elif mode == 1:#start exploring
			self.dialog_view = 0

		elif mode == 2:#for banning some game functions in mode 1(exploring mode)
			self.item_view = 1
			#TODO
			#配置一個小返回按鈕提示於角落，按下'b'回到mode 1

		elif mode == 3:
			self.dialog_view = 1
			self.manual_node = semi_manual_play_dialog(self,self.manual_dialog)
			auto_prompt(self,'->',{'x':.25,'y':.4},instance=self, prompt=True,extra_info='For next sentence...\n')

			


	def auto_seal(self, instance, seal_on):
		print('[*]auto_seal:', seal_on)
		if self.manager.current == 'story':
			if seal_on:
				print('seal_on self.pos,self.size:',self.pos,self.size)
				self.canvas.add(Color(rgba=(.2,.2,.2,.4),group='seal'))
				self.canvas.add(Rectangle(pos=(0,0),size=self.size,group='seal'))
				self.add_widget(self.chapter_title)
				print(f"Add self.chapter_title.text:{self.chapter_title.text}")
			else:	
				print('seal_off')
				print(f"Remove self.chapter_title.text:{self.chapter_title.text}")
				self.remove_widget(self.chapter_title)
				self.canvas.remove_group('seal')
				self.chapter_info.started = True	
				
	def auto_load_chapter_info_contents(self, instance, chapter_info):
		print('[*]chapter_info:', chapter_info)
		self.chapter_maps = chapter_info.chapter_maps
		#call auto_switch_maps for next round's default map?
		self.NPCs_allocation = chapter_info.chapter_NPCs#TODO: load NPCs
		self.objects_allocation = chapter_info.chapter_objects#TODO: load objects
		self.auto_dialog = self.chapter_info.pre_plot 
		self.manual_dialog = self.chapter_info.plot
		self.chapter_title = Label(text=self.chapter_info.chapter_title,color=(1,1,1,1),pos_hint={'x':.25,'y':.4},size_hint=(.5,.3),halign='center',valign='center',font_size=184,font_name='res/HuaKangTiFan-CuTi-1.otf')
		self.seal_on = not self.chapter_info.started
		self.remove_widget(self.itemframe)
		self.itemframe = ItemFrame(pos_hint = {'x':.8,'y':.25},size_hint = (.2,.6))#(pos_hint = {'x':.15,'y':.33},size_hint = (.85,.5))#parent_w=self.w,parent_h=self.h
		self.reload_item_list = True
		self.generate_item_tag()
		print('chapter_info:', chapter_info,'self.itemframe:',self.itemframe)
		
		print(f'chapter_maps:{self.chapter_maps},NPCs_allocation:{self.NPCs_allocation},objects_allocation:{self.objects_allocation},current_dialog:{self.auto_dialog}')

	def auto_new_chapter(self, instance, complete_chapter):#called when outer calls "self.complete_chapter = True"  
		if complete_chapter:
			print('[*]complete_chapter:', complete_chapter)#after the plot's dialog ended
			GM.change_chapter()
			#TODO: link to the plot of the chapter's ending
			
			self.next_round()
	#TODO: load story's dialog
	def auto_dialog_view(self, instance, dialog_view):#TODO: merge the frame and tag image
		print('[*]dialog view:', dialog_view)
		
		if dialog_view == 1:
			print("load dialog view")
			#self.current_speaker_name = GM.players_name[self.current_player_id]#TODO: decide this by the dialogs
			self.canvas.add(Rectangle(source='res/images/origin_dialogframe.png',pos=(0,0),size=(self.w*self.dialogframe_width,self.h*(self.dialogframe_height+.07)),group='dialogframe'))
		else:
			print("hide dialog view")	
			self.current_speaker_name = ''
			self.canvas.remove_group('dialogframe')

	def auto_item_view(self, instance, item_view):#Entry and Exit of all itemframe functions
		print('[*]item view:', item_view)
	
		if item_view == 1:
			self.display_itemframe()	
		else:
			self.hide_itemframe()

	#select the background image of this story	
	def auto_reload_chapter_info(self, instance, c_p):#called when outer calls "self.current_player_id, self.current_chapter = GM.change_turn()"
		print('[*]current_player_chapter: ', c_p)
		
		#load chapter info at each round starts
		self.chapter_info = GM.Chapters[self.current_player_id][self.current_chapter]
		print("reload chapter_info:",self.chapter_info)
	def auto_hp_canvas(self,instance, hp):#if hp = 0, end this round
		print('[*]hp:', hp)
		#self.canvas.remove_group('hp')
		for hp in self.hp_widgets:
			self.remove_widget(hp)
		for i in range(self.hp_per_round):
			hp = Image(source='res/images/testing/HP.png',pos_hint={'x':.94-.06*i,'y':.85},size_hint=(.04,.1))
			self.add_widget(hp)
			self.hp_widgets.append(hp)
		if hp == 0:
			popup = Popup(title='體力耗盡',title_size='28sp',title_font='res/HuaKangTiFan-CuTi-1.otf',title_color=[.2,.9,.1,.9],content=Label(text='輪到下一位玩家',font_size=64,font_name= 'res/HuaKangTiFan-CuTi-1.otf'),size_hint=(None, None), size=(400, 400))
			popup.open()
			self.next_round()                           

	def auto_switch_maps(self,instance, current_map):
		if current_map >= 0:
			print('[*]current map:', current_map)
			print("self.chapter_maps:",self.chapter_maps)
			#self.canvas.before.remove_group('bg')
			print("self.chapter_maps[current_map]:",self.chapter_maps[current_map])
			bg = Rectangle(source=self.chapter_maps[current_map], pos=(0,0), size=(self.w,self.h),group='bg')
			self.bg_widget.load_bg(bg)

			for mapobject in self.objects_allocation:
				if mapobject.map_name in self.chapter_maps[current_map]:
					self.add_widget(mapobject)
				else:
					self.remove_widget(mapobject)
			#如果有NPC也照做


	def auto_reload_item_list(self,instance, reload_item_list):
		if reload_item_list:
			print('[*] auto update instance:',reload_item_list)
			self.itemframe.item_list = GM.players[self.current_player_id].item_list
			print('reload self.itemframe.item_list:',self.itemframe.item_list)	
			self.reload_item_list = False

	def auto_focus_item(self, instance, focusing_object_id):#whenever open itemframe or switching , generate dragging object
		print('auto focus object id:',focusing_object_id)
		print('self.itemframe.cyclic:',self.itemframe.cyclic)
		
		if focusing_object_id >=0 :
			self.canvas.remove_group('itemicon') 
			#dynamic icon generate:
			s_pos = (.805*global_w,.758*global_h)
			s_size = (.19*global_w,.085*global_h)
			i_len = min(.0475*global_w,.08*global_h)
			self.canvas.add(Ellipse(pos=(s_pos[0]+(s_size[0]-i_len)/2,s_pos[1]+(s_size[1]-i_len)/2),size=(i_len,i_len),source=GM.object_table[str(focusing_object_id)]['source'],group='itemicon'))
			
			#dynamic draggable generate:
			source = GM.object_table[str(focusing_object_id)]['source']
			d_len = min(.15*global_w,.2*global_h)#FreeDraggableItem#,
			self.dragging = FreeDraggableItem(screen=self,source=source,magnet=True,size=(d_len,d_len),pos=(.75*global_w,.4*global_h),size_hint=(None,None))
			#self.add_widget(self.dragging)
				

	def key_action(self, *args):#TODO:盡量統一按鍵、做好遊戲按鍵提示介面
		if self.manager.current == 'story':	
			#print('story key: ',args)
			press_key_id = args[1]#args[1]:ASCII?
			press_key = args[3]
			if press_key_id in [276,275]:#<-,->
				if self.current_mode == 1: 
					if self.item_view == 0:
						self.exploring_maps(press_key_id)
					elif self.item_view == 1:
						if self.itemframe.switchable and self.itemframe.playing_anim_num <= 0:
							self.item_box_canvas_controller('show',direction=press_key_id) 


				if self.current_mode == 3:
					self.remove_widget(self.prompt_label)	
					self.exploring_dialog(press_key_id)

			elif press_key_id == 98:#b:
				if self.current_mode == 2:
					#self.remove_widget(self.prompt_label) 
					#TODO:將mode 2 的暫存狀態回復
					self.current_mode = 1

			elif press_key_id == 105:#i:
				self.item_view ^= 1

			elif press_key_id == 13:
				if self.seal_on and self.manager.current == 'story':
					print('Get ENTER!')
					self.seal_on = False
					self.chapter_info.started = True
					self.current_mode = 0#precursor mode entry

				elif self.current_mode == 0 and self.finish_auto:
					self.remove_widget(self.prompt_label)
					self.current_mode = 1#exploring mode entry

				elif self.current_mode == 1:
					if self.item_view == 1:
						self.itemframe.use_item(self,self.focusing_object_id,None)

				elif self.current_mode == 3:
					if self.manual_node.type == 'tail': 
						self.remove_widget(self.prompt_label) 
						for event in screen.dialog_events:
							event.cancel()	
						clear_dialogframe_text(screen,screen.displaying_character_labels)		
						self.complete_chapter = True


			#for testing
			elif press_key_id == 112:#p
				if self.current_mode == 1:	
					self.current_mode = 3
			elif press_key_id == 100:#d: 
				self.dialog_view ^= 1

			elif press_key_id == 115:#s
				if self.current_mode == 0:
					print('Skip the auto dialog')
					for event in self.dialog_events:
						event.cancel()
					clear_dialogframe_text(self,self.displaying_character_labels)
					self.finish_auto = True

			elif press_key_id == 116:#t
				if self.cur_unsafed:
					self.testing_save_object_pos()
				else:
					self.testing_set_objects_pos()
			# elif  press_key_id == 114:#r:
			# 	if self.current_mode == 1:	
			# 		if self.item_view == 0: 
			# 			self.next_round()

			elif  press_key_id == 109:#m:
				if self.current_mode == 1:
					self.complete_chapter = True
			elif  press_key_id == 110:#n:
				if self.current_mode == 1:
					if self.item_view == 0: 
						self.next_round()

			elif press_key_id in [274,273]:
				if self.cur_unsafed:
					self.testing_modify_object_size(press_key_id)
				if self.current_mode == 1: 
					pass

			return True
	def key_release(self, *args):
		if self.manager.current == 'story':	
			#print('story key release: ',args)
			press_key_id = args[1]#args[1]:ASCII?

			return True	
	def exploring_maps(self, press_key_id):

			num = len(self.chapter_maps)

			if press_key_id==276:
				print ("key action left")
				if self.current_map <= 0:
					self.current_map = num - 1
				else:
					self.current_map -= 1				
			elif press_key_id==275:
				print ("key action right")
				if self.current_map >= num - 1:
					self.current_map = 0
				else:
					self.current_map += 1

	def generate_item_tag(self):
		print("Enter function: generate_item_tag")
		#TODO: 改進效率
		#RGB (0,182,237)
		#self.itemframe = ItemFrame(pos_hint = {'x':.8,'y':.25},size_hint = (.2,.6))#(pos_hint = {'x':.15,'y':.33},size_hint = (.85,.5))#parent_w=self.w,parent_h=self.h
		#self.item_images = self.itemframe.auto_gen_items(GM.players[self.current_player_id].item_list)		
		#self.itemframe.item_list = GM.players[self.current_player_id].item_list	
		self.item_tag = ImageButton(pos_hint={'x':.97,'y':.77},size_hint=(.03,.08),source='res/images/itemtag.png',callback=self.display_itemframe,allow_stretch=True,keep_ratio=False)
		self.add_widget(self.item_tag)

	def display_itemframe(self,*args):
		print('Enter function: display_itemframe')

		self.remove_widget(self.item_tag)
		if self.itemframe not in self.children: #for exceptions
			self.add_widget(self.itemframe)
		else:
			print('[*]Exceptions: self.itemframe is already added')

		self.dialog_view = 1
			
		self.item_box_canvas_controller('show')

		self.item_tag = ImageButton(pos_hint={'x':.77,'y':.77},size_hint=(.03,.08),source='res/images/itemtag.png',callback=self.hide_itemframe,allow_stretch=True,keep_ratio=False)

		self.add_widget(self.item_tag)	
	def hide_itemframe(self,*args):
		print('Enter function: hide_itemframe')
		
		self.dialog_view = 0
		self.item_box_canvas_controller('hide')
		self.remove_widget(self.itemframe)
		self.remove_widget(self.item_tag)
		
		self.generate_item_tag()
		print('self.itemframe:',self.itemframe,'self.item_tag:',self.item_tag)

	def item_box_canvas_controller(self,action,*args,direction=None):#all canvas things about itemframe on the screen
		if action == 'show':
			self.canvas.remove_group('cap')

			self.canvas_under_item_images()

			#dynamic canvas
			if direction is not None: #choosing in itemframe
				self.itemframe.switching_frame_focus(self,direction)
			else: #just open itemframe
				for i in reversed(range(self.itemframe.count)):
					item = self.itemframe.item_images[self.itemframe.cyclic[i]]
					self.add_widget(item)			
				self.itemframe.focusing_frame_id = self.itemframe.cyclic[0]#->auto_focus->auto_focus_item->dragging generate
				#make sure the dragging is inside box canvas

			self.canvas_on_item_images()
		
			#select button

		elif action == 'hide':
			self.itemframe.focusing_frame_id = -1
			self.canvas.remove_group('cap')
			for item in self.itemframe.item_images:
				self.remove_widget(item)
			#self.canvas.remove_group('itemicon') 

	def canvas_under_item_images(self):
		# title screen
		self.canvas.add(Color(rgba=(0,110/255,.8,1),group='cap'))
		self.canvas.add(Quad(points=(.8*global_w,.75*global_h,.805*global_w,.758*global_h,.805*global_w,.843*global_h,.8*global_w,.85*global_h),group='cap'))
		self.canvas.add(Color(rgba=(0,90/255,.6,1),group='cap'))
		self.canvas.add(Quad(points=(.8*global_w,.75*global_h,.805*global_w,.758*global_h,.995*global_w,.758*global_h,global_w,.75*global_h),group='cap'))
		self.canvas.add(Color(rgba=(0,110/255,.8,1),group='cap'))
		self.canvas.add(Quad(points=(.995*global_w,.758*global_h,global_w,.75*global_h,global_w,.85*global_h,.995*global_w,.843*global_h),group='cap'))
		self.canvas.add(Color(rgba=(0,90/255,.6,1),group='cap'))
		self.canvas.add(Quad(points=(.805*global_w,.843*global_h,.8*global_w,.85*global_h,global_w,.85*global_h,.995*global_w,.843*global_h),group='cap'))
		self.canvas.add(Color(rgba=(1,1,1,.98),group='cap'))#source='res/images/itemframe.png',
		self.canvas.add(Rectangle(pos=(.805*global_w,.758*global_h),size=(.19*global_w,.085*global_h),group='cap'))
		#box
		self.canvas.add(Color(rgba=(0,100/255,.7,.98),group='cap'))
		self.canvas.add(Triangle(points=(.70*global_w,.5*global_h,.8*global_w,.5*global_h,.8*global_w,.55*global_h),group='cap'))

	def canvas_on_item_images(self):
		self.canvas.add(Color(rgba=(0,182/255,1,1),group='cap'))#source='res/images/itemframe.png',
		self.canvas.add(Rectangle(pos=(.70*global_w,.2*global_h),size=(.2*global_w,.3*global_h),group='cap'))
		self.canvas.add(Color(rgba=(0,100/255,.7,1),group='cap'))
		self.canvas.add(Quad(points=(.90*global_w,.2*global_h,.90*global_w,.5*global_h,global_w,.55*global_h,global_w,.25*global_h),group='cap'))


	def exploring_dialog(self, press_key_id):
			if press_key_id==276:
				print ("key action left")
				self.last_dialog()
			elif press_key_id==275:
				print ("key action right")
				self.next_dialog()
			print('self.manual_node.text_line:',self.manual_node.text_line)	#為何都會自動消失
	def next_dialog(self,*args):
		if self.manual_node.type != 'tail':
			for event in self.dialog_events:
				event.cancel()
			clear_dialogframe_text(self,self.displaying_character_labels)
			node = self.manual_node = self.manual_node.get_next()
			self.lastline_time = line_display_scheduler(self,speaker_name[node.speaker],node.text_line,False,special_char_time,next_line_time,common_char_time)
		else:
			#prompt to next chapter, end round
			auto_prompt(self,'Enter',{'x':.25,'y':.4},instance=self, prompt=True,extra_info='Complete chapter!\n')

	def last_dialog(self,*args):		
		if self.manual_node.type != 'head':
			for event in self.dialog_events:
				event.cancel()
			clear_dialogframe_text(self,self.displaying_character_labels)
			node = self.manual_node = self.manual_node.get_last()
			self.lastline_time = line_display_scheduler(self,speaker_name[node.speaker],node.text_line,False,special_char_time,next_line_time,common_char_time)

	def enter_puzzle_mode(self, object_id, behavior_type):#在道具欄使用道具進入的puzzle_mode跟地圖上點擊有何不同
		self.current_mode = 2
		if behavior_type == 'puzzle':
			self.puzzle_handler(object_id)
		elif behavior_type == 'lock': 
			self.lock_handler(object_id)
		elif behavior_type == 'synthesis': 
			self.synthesis_handler(object_id)

		
	def puzzle_handler(self, object_id):
		pass	
	def lock_handler(self, object_id):
		pass	
	def synthesis_handler(self, object_id):
		pass	

	#TODO: implement object functions here, btn must be an instance of MapObject()
	def on_press_item(self, btn):
		object_id = btn.object_id
		print("Before self.reload_item_list:",self.reload_item_list)
		GM.players[self.current_player_id].get_item(object_id)
		print("After self.reload_item_list:",self.reload_item_list)
		self.remove_widget(btn) 
		self.dialog_view = 1
		spent_time = line_display_scheduler(self,'','撿到不錯的東西了呦\n',False,special_char_time,next_line_time,common_char_time)
		self.delay_hide_dialogframe(2+spent_time)
	def on_press_puzzle(self, btn):
		#查解碼表
		puzzle_bg = btn.puzzle_bg(btn.source )
		bg = Rectangle(source=puzzle_bg, pos=(0,0), size=(self.w,self.h),group='puzzle_bg')
		#bg = Rectangle(source=self.chapter_maps[self.current_map], pos=(0,self.h*self.dialogframe_height), size=(self.w,self.h*(1-self.dialogframe_height)),group='bg')
		self.bg_widget.load_bg(bg)

	def on_press_lock(self,btn):

		pass

	def on_press_synthesis(self,btn):
		pass

	def on_press_trigger(self,btn):
		self.current_mode = 3

	def on_press_clue(self, btn):
		#self.clue_Label = Label()
		self.dialog_view = 1
		#self.add_widget(clue_Label) 
		text_line = GM.object_table[str(btn.object_id)]['description'][:20]
		spent_time = line_display_scheduler(self,'',text_line,False,special_char_time,next_line_time,common_char_time)
		self.delay_hide_dialogframe(3.5+spent_time)

	def on_press_switching(self,btn):#TODO:統一格式
		new_scene_name = GM.object_table[str(btn.object_id)]['description'].split('\'')[1]
		for i,img in enumerate(self.chapter_maps):
			if new_scene_name in img:
				self.current_map = i
	def on_press_nothing(self, btn):
		self.dialog_view = 1
		#self.add_widget(self.nothingLabel) 
		spent_time = line_display_scheduler(self,'','好像有東西在這裡...但看不出用途...\n',False,special_char_time,next_line_time,common_char_time)
		self.delay_hide_dialogframe(2+spent_time)

	def delay_hide_dialogframe(self, delay_time):#delay_time unit:seconds

		def delay_close_dialog_view(screen,dt):
			screen.dialog_view = 0
		Clock.schedule_once(partial(clear_dialogframe_text,self,self.displaying_character_labels),delay_time)
		Clock.schedule_once(partial(delay_close_dialog_view,self),delay_time+0.1)

	def to_phone_screen(self,*args):
		if self.current_mode == 1:
			self.manager.current = 'phone'

	#for testing: 	
	def to_game_screen(self,*args):
		if self.current_mode == 1:
			subgames_id = 0#decided by story
			self.manager.current = 'subgames_manager'
			if not self.manager.get_screen('subgames_manager').initialized:
				self.manager.get_screen('subgames_manager').init_all_subgames()
			self.manager.get_screen('subgames_manager').start_subgame_id(subgames_id)
			

	#for testing: drag objects to map location and save
	def testing_objects_path_init(self):
		import shutil
		self.testing_objects = []
		self.testing_objects_id = -1
		dir_path = 'res/images/unlocated_mapobjects/' 
		paint_path = 'res/images/handpainting/'

		for origin in os.listdir(dir_path):
			os.remove(os.path.join(dir_path,origin))
		#
		allocated_data = {}
		if os.path.isfile('res/allocate_all_objects_table.json'):
			f = open('res/allocate_all_objects_table.json','r')
			allocated_data = json.load(f)
			print('exist allocated_data before testing:',allocated_data)
			f.close()

		#load unlocated mapobjects
		for key,item in GM.object_table.items():
			for img_name in os.listdir(paint_path):
				if item['on_map'] and item['name'] in img_name and item['name'] not in allocated_data.keys():
					shutil.copy(os.path.join(paint_path,img_name),dir_path)
					
		#generate testing objects			
		files = os.listdir(dir_path)
		for f in files:
			if '.jpg' in f or '.png' in f:
				fulldir_path = os.path.join(dir_path,f)
				if os.path.isfile(fulldir_path):
	 				self.testing_objects.append(fulldir_path)	
		print('testing objects:',self.testing_objects)		
		self.cur_unsafed = False	
	#for testing: drag objects to map location and save, same for NPC or other undetermined widgets
	def testing_set_objects_pos(self):
		if self.testing_objects_id > len(self.testing_objects)-2:
			return 
		else:
			self.testing_objects_id += 1
		source=self.testing_objects[self.testing_objects_id]
		print('testing source:',source)
		self.cur_testing_dragitem = FreeDraggableItem(pos=(0,0),size=(100,100),source=source,size_hint=(None,None))
		self.add_widget(self.cur_testing_dragitem)
		self.cur_unsafed = True
	#for testing: drag objects to map location and save	
	def testing_save_object_pos(self):
		data = {}
		if os.path.isfile('res/allocate_all_objects_table.json'):
			f = open('res/allocate_all_objects_table.json','r')
			data = json.load(f)
			print('exist data:',data)
			f.close()
		pos_hint = self.cur_testing_dragitem.stopped_pos_hint
		size_hint = (self.cur_testing_dragitem.size[0]/global_w,self.cur_testing_dragitem.size[1]/global_h)
		source = self.testing_objects[self.testing_objects_id].replace('unlocated_mapobjects','handpainting')
		#write: player_id,chapter_id,mapid,object_pos_hint, source	
		item_name = source.split('/')[-1].split('.')[0]

		data[item_name] = {'pos_hint':pos_hint,'size_hint':size_hint,'source':source}
		print(f'Save data[{item_name}]: {data[item_name]}!')
		with open('res/allocate_all_objects_table.json','w') as f:	
			json.dump(data, f)
		self.remove_widget(self.cur_testing_dragitem)
		#f.write(f'player_id:{self.current_player_id},chapter_id:{self.current_chapter},mapid:{self.current_map},object_pos_hint:{pos_hint},object_size_hint:{size_hint},source:{source}\n')
		#f.close()
		self.cur_unsafed = False
	def testing_modify_object_size(self, press_key_id):
		if press_key_id == 274:
			self.cur_testing_dragitem.size[0] -= 10
			self.cur_testing_dragitem.size[1] -= 10
		elif press_key_id == 273:
			self.cur_testing_dragitem.size[0] += 10
			self.cur_testing_dragitem.size[1] += 10
	#for testing: 
	def testing_golden_finger(self):
		pass


	#TODO
	def load_game(self):
		self.next_round()
		# if os.path.isfile('res/game_archive.json'):
		# 	GM.load_game()
		
		
	def save_game(self):
		GM.save_game()


	@staticmethod
	def exit_game():
		exit()
