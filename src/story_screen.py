###################################################
# Main screen of this game                        #
###################################################
from game_manager import *

GM = GameManagerScreen()
global_x = 0
global_y = 0

class ItemFrame(FloatLayout):

	parent_w = NumericProperty()
	parent_h = NumericProperty()
	focusing_frame_id = NumericProperty(-1)
	item_list = ListProperty([])
	switchable = BooleanProperty(True)
	playing_anim_num = NumericProperty()
	def __init__(self,screen,**kwargs):
		super(ItemFrame, self).__init__(**kwargs)
		print(f"init itemframe global_w:{global_w},global_h:{global_h},self.size:{self.size},self.parent={self.parent}:")

		self.parent_w = global_w
		self.parent_h = global_h
		self.infoFrame = Widget()
		self.item_name = Widget()
		self.infoContent = Widget()
		self.screen = screen
		self.bind(item_list=self.auto_gen_items)#after auto_reload_item_list called
		self.bind(focusing_frame_id=self.auto_focus)
		self.bind(playing_anim_num=self.auto_switchable)

		self.front_pos = (.75*global_w,.4*global_h)
		self.back_pos = (.85*global_w,.45*global_h)#for animations

		self.offset = (0,0)
		self.count = 0
		self.item_size = (.04*global_w,.06*global_h)
		self.info_size_x, self.info_size_y = .12*global_w,.18*global_h
		self.cyclic = {}
		self.item_images = []
	def auto_switchable(self,instance,playing_anim_num):
		print('[*] playing_anim_num:',playing_anim_num)
		if playing_anim_num > 0:
			self.switchable = False
		else: 
			self.switchable = True

	def auto_gen_items(self,instance,item_list):#focusing_frame_id must be self.cyclic[0] when first open the frame after modified item_list
		print('[*]item frame gen items:',item_list)
		self.count = len(item_list)
		print("item_list:",item_list)
		if self.count > 1:
			self.offset = (.1/(self.count-1)*global_w,.05/(self.count-1)*global_h)
		item_cur_pos = []
		for i in range(self.count):
			#print('test append pos:',(.75*global_w + i*self.offset[0]),(.4*global_h+i*self.offset[1]))
			item_cur_pos.append([(.75*global_w + i*self.offset[0]),(.4*global_h+i*self.offset[1])])
		d_len = min(.15*global_w,.2*global_h)
	
		for ci in self.item_images :
			self.screen.remove_widget(ci)
		self.item_images = [CircleImage(pos=item_cur_pos[i],size_hint=(None,None),size=(d_len,d_len) ,source=GM.object_table[str(object_id)]['source']) for i,object_id in enumerate(item_list)] 	
		#item_images與item_list共用focusing_frame_id, 另開一個循環id用來展示選取動畫
		#when item_images modified, manually modified the item_list
		
		for i in range(self.count):
			self.cyclic[i] = i

	#dynamic generate part:	
	def auto_focus(self, instance, focusing_frame_id):#handle the info and object id
		print('auto focus frame id:',focusing_frame_id)
		print('current self.item_list:',self.item_list)
		screen = self.screen
		object_id = self.item_list[focusing_frame_id]
		#clear the last status
		screen.remove_widget(self.item_name)
		screen.clear_text_on_screen()
		if focusing_frame_id >= 0:	

			if screen.current_mode == 1:
				self.display_item_info(object_id,screen)
				self.display_item_name(object_id,screen)
			elif screen.current_mode == 2:
				self.display_item_name(object_id,screen)
			screen.focusing_object_id = object_id
		else:
			print('when close itemframe, screen:',screen)
			#screen.remove_widget(self.item_name)
			screen.focusing_object_id = -1

	def display_item_name(self,object_id,screen):
		#screen.remove_widget(self.item_name)
		self.item_name = Label(text= GM.object_table[str(object_id)]['name'],pos_hint={'x':0,'y':.2},color=(.7,1,.4,1),font_size=30,size_hint=(.26,.07),font_name= 'res/HuaKangTiFan-CuTi-1.otf')
		screen.add_widget(self.item_name)
	def display_item_info(self,object_id,screen):
		print('auto_display_item_info object_id:',object_id)
		text_line = GM.object_table[str(object_id)]['description']
		if len(text_line) == 0:
			text_line = '不明道具...不知道可以用來做什麼\n'
		print('text_line:',text_line)
		spent_time = line_display_scheduler(screen,text_line,False,.2,.5,.15)
			
	def switching_frame_focus(self,screen,press_key_id):#handle the cyclic animation
		#self.switchable = False
		

		n = self.playing_anim_num = self.count #determined by the number of animations
		screen.try_open_item_view()
		#n = self.count
		if n > 1:
			d_len = min(.15*global_w,.2*global_h)

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

			elif press_key_id==275:
				print ("key action right")

				#store last pos:	
				final_pos = self.back_pos
				init_pos = self.front_pos
				self.curve_animation(screen,self.item_images[self.cyclic[0]],init_pos,final_pos)
				for i in range(1,n):
					im = self.item_images[self.cyclic[i]]
					im.start_switching_animate(im.pos,self.offset,'negative')

				#redraw for the correctness of overlapped order	and update the cyclic indice
				for i in reversed(range(n)):
					self.cyclic[i] += 1
					self.cyclic[i] %= n
					screen.remove_widget(self.item_images[self.cyclic[i]])
					screen.add_widget(self.item_images[self.cyclic[i]])

				#By definition, cyclic[0] = focusing_frame_id	
				if self.focusing_frame_id >= n - 1:
					self.focusing_frame_id = 0
				else:
					self.focusing_frame_id += 1				


			print('self.cyclic:',self.cyclic,'self.playing_anim_num:',self.playing_anim_num)

		#self.switchable = True


	def curve_animation(self,screen,animatable_im,init_pos,final_pos):#TODO: 修改動畫逼近曲線
		ix,iy = init_pos
		fx,fy = final_pos
		(mx,my) = middle_pos = ((ix+fx)/2 + abs((iy-fy)/2), (iy+fy)/2 - abs((ix-fx)/2))
		print('middle_pos:',middle_pos)
		offset_1 = (mx-ix,my-iy)
		offset_2 = (fx-mx,fy-my)
		if fy > iy:
			animatable_im.start_switching_animate(animatable_im.pos,[offset_1,offset_2],None,duration=[.3,.2])
		else:
			animatable_im.start_switching_animate(animatable_im.pos,[offset_1,offset_2],None,duration=[.2,.3])

	def use_item(self,screen,object_id,touch=None,*args):#the entry of using items in itemframe, behave samely as click on the itemframe focusing item
		print("use item args:",args)#self.parent.current_mode == 1 here
		item = GM.object_table[str(object_id)]	
		types = item['function_types']

		if len(types) == 1:#'item' only, 
			
			if touch is not None:
				print("拖曳普通道具!")
				screen.add_widget(screen.dragging)
				screen.dragging.on_touch_down(touch)
			else:
				print("普通道具，無法單獨使用!")
				screen.clear_text_on_screen()
				spent_time = line_display_scheduler(screen,'普通道具，無法單獨使用!\n',False,special_char_time,next_line_time,common_char_time)

		else :#type:trigger, lock, puzzle, synthesis 原則上剩一種
			if screen.current_mode == 1:
				if 'trigger' in types:
					print('觸發劇情!進入劇情模式!')
					screen.current_mode = 3
					return
				behavior_type = [t for t in types if t != 'item'][0]
				screen.enter_puzzle_mode(object_id, behavior_type)		

			elif screen.current_mode == 2:
				if touch is not None:
					print("拖曳道具!")
					screen.add_widget(screen.dragging)
					screen.dragging.on_touch_down(touch)

	def on_touch_down(self, touch):
		print('itemframe touch.profile:',touch.profile,'touch.id:',touch.id,'touch.pos:',touch.pos)
		if self.parent is not None and self.focusing_frame_id >= 0 and self.item_images[self.focusing_frame_id].collide_point(*touch.pos) and self.count > 0:
			object_id = self.item_list[self.focusing_frame_id]
			screen = self.parent
			self.use_item(screen,object_id,touch)




class StoryScreen(Screen):

	current_player_id = NumericProperty()
	current_chapter = NumericProperty(-1)
	current_player_chapter = ReferenceListProperty(current_player_id, current_chapter)
	current_map_id = NumericProperty(-1)
	chapter_maps = ListProperty()#need to bind?
	current_speaker_name = StringProperty('N')
	hp_per_round = NumericProperty(30)
	w = NumericProperty(100)
	h = NumericProperty(100) 
	button_width = NumericProperty(0.08)
	dialogframe_width = NumericProperty(0.92)	
	dialogframe_height = NumericProperty(0.2)
	button_height = NumericProperty(0.125) 
	bg_height = NumericProperty(0.8)
	item_list = ListProperty([])
	end_round = BooleanProperty(False)
	complete_chapter = BooleanProperty(False)
	bg_widget = ObjectProperty(Widget())
	itemframe = ObjectProperty(Widget())
	dialog_view = NumericProperty(0)#0:background view(exploring maps), 1:dialog view
	item_view = NumericProperty(0)#0:background view(exploring maps), 1:item view
	NPC_view = NumericProperty(0)#0:background view(exploring maps), 1:item view
	dialogframe_mutex = NumericProperty(0)#ReferenceListProperty(item_view,NPC_view)#TODO: mutex lock
	chapter_info = ObjectProperty()#rebind=True
	seal_on = BooleanProperty(False)
	current_mode = NumericProperty(-1)#0:precursor mode, 1:exploring mode, 2: puzzle mode, 3:plot mode
	finish_auto = BooleanProperty(False)
	nametag = ObjectProperty(Label())
	dialog_events = ListProperty([])
	reload_item_list = BooleanProperty(False)
	focusing_object_id = NumericProperty(-1)
	dragging = ObjectProperty(FreeDraggableItem(source=''))
	puzzling = BooleanProperty(False)
	answer_code = ListProperty([])
	current_scene = StringProperty('')
	behavior_type = StringProperty('')
	probing = BooleanProperty(False)
	loading = BooleanProperty(True)
	NPC_talking = BooleanProperty(False) 
	text_cleared = BooleanProperty(True) 
	judgable = BooleanProperty(True) 
	in_judge_range = BooleanProperty(False) 
	current_player = StringProperty()
	unread_count = NumericProperty(0)
	golden_id = NumericProperty(0)
	golden_password = StringProperty('geniuspudding')
	cheat_chapter_id = NumericProperty(0)
	cheat_chapter_password = StringProperty('koreanogoodfish')
	current_line = StringProperty('')
	current_char_id = NumericProperty(0)
	display_pausing = NumericProperty(0)#0:not in auto dialog, 1:auto displaying, 2: auto pausing

	#initialize of the whole game, with fixed properties and resources
	def __init__(self, **kwargs):
		super(StoryScreen, self).__init__(**kwargs)
	def start_story(self,linked_GM):
		global GM
		GM = linked_GM

		self.size = (self.w,self.h) = (global_w,global_h)#get_screen_size()
		print(f"global_w:{global_w},global_h:{global_h}")	
		self.button_height = self.dialogframe_height/2
		print("init pos={},size={},self={},type(self)={},(w,h)={},Window.size={}".format(self.pos,self.size,self,type(self),(self.w,self.h),Window.size))
		self.bind(current_speaker_name=partial(auto_display_speaker,self))
		self.bind(current_map_id=self.auto_switch_maps)
		#self.bind(current_map_id=self.auto_save_game)
		#self.bind(current_player_chapter=self.auto_reload_chapter_info)
		self.bind(chapter_info=self.auto_load_chapter_info_contents)
		self.bind(dialog_view=self.auto_dialog_view)
		self.bind(item_view=self.auto_item_view)
		self.bind(NPC_view=self.auto_NPC_view)
		self.bind(complete_chapter=self.auto_end_chapter)
		self.bind(seal_on=self.auto_seal)
		self.bind(current_mode=self.auto_switch_mode)
		self.bind(finish_auto=partial(auto_prompt,self,'Enter',{'x':.2,'y':.3},pre_info='至此，命運之輪將不再停止...'))
		self.bind(finish_auto=self.auto_start_chapter)
		self.bind(reload_item_list=self.auto_reload_item_list)
		self.bind(focusing_object_id=self.auto_focus_item)
		self.bind(NPC_talking=self.auto_listen)
		self.bind(golden_id=self.auto_golden_player)
		self.bind(cheat_chapter_id=self.auto_cheat_chapter)
		self.bind(text_cleared=self.auto_check_text_cleared)
		self.bind(unread_count=self.auto_unread_notation)
		Window.bind(on_key_down=self.key_action)
		self.hp_widgets = []
		self.displaying_character_labels = []
		self.lock = Image()
		self.chapter_title = Label()
		self.mapobjects_register = []
		self.mapNPC_register = []
		self.objects_allocation = [[]]
		self.NPCs_allocation = [[]]
		self.prompt_label = Label()
		self.unread_label = Label()
		#self.nametag = Label()#(Image(),Label())
		sub_size = max(self.w*self.button_width*.6,self.h*self.button_height*.8)
		#self.subgame_button = ImageButton(callback=self.to_game_screen,source='res/images/testing/subgame_icon.png',pos_hint={'x':self.dialogframe_width+self.button_width-sub_size/self.w,'y':self.dialogframe_height},size_hint=(sub_size/self.w,sub_size/self.h))
		self.banned_map_list = ['女主書桌','A女書桌','女主書桌抽屜','女主家裡房間保險箱']#skip when switching maps 
		self.NPC_tag = Image(pos_hint={'x':.94,'y':.55},size_hint=(.06,.15),source='res/images/NPC_tag.png',allow_stretch=True,keep_ratio=False)

		self.bg_widget = BG_widget(parent =self)
		self.add_widget(self.bg_widget) 

		# self.canvas.add(Color(rgba=(1,1,1,1),group='switch_map'))
		# self.canvas.add(Rectangle(source='res/images/switch_map.png',pos=(.4*global_w,0),size=(.2*global_w,.2*global_h),group='switch_map'))

		self.next_round()
		#self.load_game() #testing auto load/save this game, or set a button

	#the entry of main function in each round 	
	def next_round(self,*args):
		print("Enter function: next_round")
		#<clear the last round status>: 清除前一位玩家回合狀態 	
		self.map_objects_allocator('deallocate')
		self.end_round = False#TODO: if true, 出現輪下一位玩家的按鈕或按鍵提示
		self.complete_chapter = False
		self.switch_id = 0
		#for testing
		#self.remove_widget(self.subgame_button)

		#<modify game info>: 配置回合切換所需 
		self.current_player_id, self.current_chapter = GM.change_turn()#Then call auto_reload_chapter_info, and then bind auto_load_chapter_info_contents
		#陷阱!!!有先後順序 會auto_reload_chapter_info兩次 
		print("player:{}, chapter:{} ,self.size:{}".format(self.current_player_id, self.current_chapter,self.size))		
		self.auto_reload_chapter_info(self,[self.current_player_id, self.current_chapter])
		self.current_player = player_name[self.current_player_id]

		#round-binding canvas: 
		self.hp_per_round = 20#trigger event #auto save?

		#<chapter info part>: 透過bind auto_load_chapter_info_contents，從 chapter_info 載入所有地圖所需
		# self.current_map_id = -2
		# self.current_map_id = self.chapter_info.chapter_default_map #0#trigger the map loading function

		#auto save
		# if self.finish_auto:
		# 	self.auto_save_game()

	def auto_switch_mode(self, instance, mode):#Entry of all stroy screen modes
		print('[*]Switch mode:', mode)
		if mode == 0:#For each chapter starts
			self.seal_on = True

		elif mode == 1:#start exploring
			Clock.schedule_once(self.try_close_dialog_view,.8)

			#start exploring mode, allocate objects on chapter's map 
			#testing
			Clock.schedule_once(partial(self.map_objects_allocator,'reallocate'),.8)			

		elif mode == 2:#for banning some game functions in mode 1(exploring mode)
			self.item_view = 1

		elif mode == 3:
			if self.item_view == 1:
				self.item_view = 0#self.map_objects_allocator('deallocate')
				self.map_objects_allocator('deallocate')

			self.try_open_dialog_view()	
			print('try_open_dialog_view')

			self.manual_node = semi_auto_play_dialog(self,self.plot_dialog)
			self.remove_widget(self.prompt_label)#for exception!
			auto_prompt(self,'->',{'x':.2,'y':.3},instance=self, prompt=True,pre_info='回憶似海，若你無意靠岸...',post_info='越沉...越深...')

		self.auto_save_game()	

	def auto_seal(self, instance, seal_on):
		print('[*]auto_seal:', seal_on, 'self.manager.current:', self.manager.current)
		if self.manager.current == 'story':#for waiting the screen switch to first chapter 
			if seal_on:
				self.canvas.add(Color(rgba=(.2,.2,.2,.4),group='seal'))
				self.canvas.add(Rectangle(pos=(0,0),size=self.size,group='seal'))
				self.add_widget(self.chapter_title)
				print(f"Add self.chapter_title.text:{self.chapter_title.text}")

			else:	
				print(f"Remove self.chapter_title.text:{self.chapter_title.text}")
				self.remove_widget(self.chapter_title)
				self.canvas.remove_group('seal')
				#self.finish_auto = False
				self.dialog_view = 1	
				auto_play_dialog(self,self.auto_dialog)
				
	def auto_load_chapter_info_contents(self, instance, chapter_info):
		print('[*]Auto load chapter_info for new round!')
		if not chapter_info.started:#finish_auto
			self.finish_auto = False
			self.chapter_title = chapter_info.chapter_title
			self.current_mode = 0
		else:
			self.current_mode = 1
		self.chapter_maps = chapter_info.chapter_maps
		self.objects_allocation = chapter_info.chapter_objects_of_maps
		self.NPCs_allocation = chapter_info.chapter_NPCs_of_maps#Mostly empty 
		self.auto_dialog = chapter_info.chapter_pre_plot 
		self.plot_dialog = chapter_info.chapter_plot
		self.scenes = chapter_info.chapter_plot_scenes
		self.plot_scenes_table = chapter_info.chapter_scenes_table
		self.picked_list = chapter_info.picked_item_info

		self.remove_widget(self.itemframe)
		self.itemframe = ItemFrame(screen = self,pos_hint = {'x':.8,'y':.25},size_hint = (.2,.6))
		self.reload_item_list = True
		self.generate_item_tag()
	
		self.current_map_id = -2
		self.current_map_id = chapter_info.chapter_default_map #0#trigger the map loading function
		
		self.unread_count = -1
		self.unread_count = len(GM.players[self.current_player_id].unread_achievement)

		print(f'chapter_maps:{self.chapter_maps},objects_allocation:{self.objects_allocation}')

	def auto_reload_chapter_info(self, instance, c_p):#do not bind "self.current_player_id, self.current_chapter = GM.change_turn()" !
		print('[*]current_player_chapter: ', c_p)
		self.chapter_info = GM.Chapters[self.current_player_id][self.current_chapter]#load chapter info at each round starts
		print("chapter_info reloaded:",self.chapter_info)

	def auto_start_chapter(self, instance, finish_auto):
		if finish_auto:
			print('testing finish_auto')
			self.display_pausing = 0
			GM.start_chapter() #let self.chapter_info.started = True
			self.loading = False

	def auto_end_chapter(self, instance, complete_chapter):#called when outer calls "self.complete_chapter = True"  
		if complete_chapter:
			print('[*]complete_chapter:', complete_chapter)#after the plot's dialog ended
			GM.change_chapter()
			
			self.next_round()

	def auto_dialog_view(self, instance, dialog_view):
		print('[*]dialog view:', dialog_view)
		
		if dialog_view == 1:
			print("load dialog view")
			self.canvas.add(Color(rgba=(1,1,1,1),group='dialogframe'))
			self.canvas.add(Rectangle(source='res/images/new_dialogframe.png',pos=(0,0),size=(self.w*self.dialogframe_width,self.h*(self.dialogframe_height+.07)),group='dialogframe'))
		elif dialog_view == 0:
			print("hide dialog view")	
			self.current_speaker_name = 'N'
			self.clear_text_on_screen()
			self.canvas.remove_group('dialogframe')


	def auto_item_view(self, instance, item_view):#Entry and Exit of all itemframe functions
		print('[*]item view:', item_view)
		if item_view == 1:
			self.map_objects_allocator('deallocate')
			self.display_itemframe()	
		elif item_view == 0:
			self.hide_itemframe()
			self.map_objects_allocator('allocate')

	def auto_NPC_view(self, instance, NPC_view):
		print('[*]NPC view:', NPC_view)
		if NPC_view == 1:
			self.map_objects_allocator('deallocate')
			self.map_NPCs_allocator('allocate')
		elif NPC_view == 0:
			self.map_NPCs_allocator('deallocate')
			self.map_objects_allocator('allocate')


	# def auto_hp_canvas(self,instance, hp):#if hp = 0, end this round
	# 	print('[*]hp:', hp)
	# 	for hp in self.hp_widgets:
	# 		self.remove_widget(hp)
	# 	for i in range(self.hp_per_round):
	# 		hp = Image(source='res/images/testing/HP.png',pos_hint={'x':.94-.04*i,'y':.85},size_hint=(.03,.1))
	# 		self.add_widget(hp)
	# 		self.hp_widgets.append(hp)
	# 	if self.hp_per_round <= 0:
	# 		self.quit_puzzle_mode()
	# 		#TODO:check if there is any status not be cleared
	# 		auto_prompt(self,'Enter',{'x':.2,'y':.3},instance=self, prompt=True,pre_info='體力耗盡!\n')		                         

	def auto_switch_maps(self,instance, current_map_id):
		if current_map_id >= 0:
			print('[*]current map:', current_map_id)
			print("self.chapter_maps[current_map_id]:",self.chapter_maps[current_map_id])
			self.bg_widget.load_bg(self.chapter_maps[current_map_id])
			if self.item_view == 1:
				self.item_view == 0
			if self.current_mode in [1,2]:
				self.map_objects_allocator('reallocate')

			if self.NPCs_allocation[self.current_map_id] != []:	
				try:
					self.add_widget(self.NPC_tag)
				except:
					print('self.NPC_tag already loaded')
			else:
				self.remove_widget(self.NPC_tag)	

			self.canvas.remove_group('switch_map')
			if len(set([map_path.split('/')[-1].split('.')[0] for map_path in self.chapter_maps])\
				-set(self.banned_map_list)) > 1:#display hint if it's able to switch maps freely in this chapter
				print('self.banned_map_list:',self.banned_map_list)
				self.canvas.add(Color(rgba=(1,1,1,1),group='switch_map'))
				self.canvas.add(Rectangle(source='res/images/switch_map.png',pos=(.4*global_w,0),size=(.2*global_w,.2*global_h),group='switch_map'))

			self.auto_save_game()

	def auto_reload_item_list(self,instance, reload_item_list):
		if reload_item_list:
			print('[*] auto update instance:',reload_item_list)
			self.itemframe.item_list = GM.players[self.current_player_id].item_list #->auto_gen_items
			print('reload items:',self.itemframe.item_list)	
			self.auto_save_game()
			self.reload_item_list = False

	def auto_focus_item(self, instance, focusing_object_id):#whenever open itemframe or switching , generate dragging object
		print('auto focus object id:',focusing_object_id)
		print('self.itemframe.cyclic:',self.itemframe.cyclic)
		
		if focusing_object_id >= 0:
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

		else:
			for item in self.itemframe.item_images:
				self.remove_widget(item)	

	def auto_listen(self,instance,NPC_talking):
		print('[*] auto listening NPC:',NPC_talking)
		if NPC_talking:
			#self.remove_widget(self.prompt_label)
			self.try_open_dialog_view()
		else:
			self.clear_text_on_screen()
			self.text_cleared = True

	def auto_check_text_cleared(self,instance,text_cleared):
		print('[*] text cleared:',text_cleared)

	def auto_unread_notation(self,instance,unread_count):
		self.canvas.remove_group('unread')
		self.remove_widget(self.unread_label)
		if unread_count > 0:

			self.canvas.add(Color(rgba=(1,0,0,1),group='unread'))
			self.canvas.add(Ellipse(pos=(self.w*.975,self.h*self.button_height*1.85),size=(15,15),group='unread'))
			self.unread_label = Label(pos_hint={'x':.975, 'y':self.button_height*1.85},size_hint=(15/self.w, 15/self.h)\
				,text=str(unread_count),color=(1,1,1,1))
			self.add_widget(self.unread_label)

	def key_action(self, *args):
		if self.manager.current == 'story':	
			print('story key: ',args)
			press_key_id = args[1]#args[1]:ASCII
			press_key = args[3]

			if self.current_mode == 1:
				if self.cheat_chapter_id < len(self.cheat_chapter_password):
					if press_key == self.cheat_chapter_password[self.cheat_chapter_id]:
						self.cheat_chapter_id += 1
						return True
					else:
						self.cheat_chapter_id = 0

			if self.current_mode == 1:
				if self.golden_id < len(self.golden_password):
					if press_key == self.golden_password[self.golden_id]:
						self.golden_id += 1
						return True
					else:
						self.golden_id = 0

			if press_key_id in [276,275]:#<-,->
				print('press_key_id in [276,275] self.current_mode:',self.current_mode)

				if self.current_mode == 1:	
					if self.item_view == 0 and self.NPC_view == 0 :
						if self.displaying_character_labels == [] and self.dialog_events == [] and \
							not self.chapter_maps[self.current_map_id].split('/')[-1].split('.')[0] in self.banned_map_list:
							self.exploring_maps(press_key_id)
						else:
							pass#TODO:加速撥放功能?

					elif self.item_view == 1:
						if self.itemframe.switchable and self.itemframe.count > 1:
						#if self.itemframe.switchable and self.itemframe.playing_anim_num <= 0 and self.itemframe.count > 1:
							self.item_box_canvas_controller('show',direction=press_key_id) 
						else:
							print('Wait for item canvas finish')
				elif self.current_mode == 2:
					if not self.puzzling:
						if self.itemframe.switchable:
						#if self.itemframe.switchable and self.itemframe.playing_anim_num <= 0:
							self.item_box_canvas_controller('show',direction=press_key_id) 
					else:		
						puzzle_move_view(self,press_key_id)

				elif self.current_mode == 3:

					self.remove_widget(self.prompt_label)	
					self.exploring_dialog(press_key_id)

			elif press_key_id in [274,273]:
				if self.puzzling:
					self.puzzle_select_number(press_key_id)		

			elif press_key_id == 98:#b:
				if self.current_mode == 2:
					self.quit_puzzle_mode()

			elif press_key_id == 99:#c:
				if self.NPCs_allocation[self.current_map_id] == []:
					return True

				if self.current_mode == 1 and self.item_view == 0:
					if self.NPC_view == 0:
						self.remove_widget(self.NPC_tag)
						self.NPC_view = 1

					elif self.NPC_view == 1:
						if not self.NPC_talking:#self.text_cleared or , testing
							self.NPC_view = 0
							self.add_widget(self.NPC_tag)

			elif press_key_id == 105:#i
				if self.current_mode == 1 and self.NPC_view == 0:
					if self.item_view == 0 and self.text_cleared and not self.probing:
						self.item_view = 1
					elif self.item_view == 1 and self.itemframe.switchable:
						self.item_view = 0

			elif press_key_id == 13:#Enter
				if self.seal_on and not self.finish_auto and self.manager.current == 'story':
					self.seal_on = False

				elif self.current_mode == 0 and self.finish_auto:
					self.clear_text_on_screen()
					self.remove_widget(self.prompt_label)
					self.current_mode = 1#exploring mode entry

				# elif self.hp_per_round <= 0:
				# 	self.next_round()  

				elif self.current_mode == 1:
					if self.item_view == 1 and self.itemframe.count > 0:
						self.itemframe.use_item(self,self.focusing_object_id,None)

				elif self.current_mode == 2:
					if not self.prompt_label in self.children:
						print('Give up the puzzle, back to exploring mode')
						self.quit_puzzle_mode()

				elif self.current_mode == 3:
					if self.manual_node.type == 'tail': 
						self.remove_widget(self.prompt_label) 
						self.clear_text_on_screen()		
						self.complete_chapter = True

			elif press_key_id == 113:#q		
				if self.current_mode == 2 or (self.current_mode == 1 and self.cheat_chapter_id == len(self.cheat_chapter_password)):	
					self.remove_widget(self.prompt_label)
					self.current_mode = 3

			elif press_key_id == 100:#d 
				if self.text_cleared and self.current_mode == 1:
					self.try_close_dialog_view()
					self.text_cleared = False
			
			elif press_key_id == 103:#g
				if self.golden_id >= len(self.golden_password):
					self.remove_widget(self.prompt_label)
					GM.ready_to_ending()

			elif press_key_id == 111:#o
				if self.current_mode == 0 and not self.seal_on and not self.finish_auto:
					if self.display_pausing == 1:
						auto_accelerate(self,prompt = True)
				elif self.current_mode in [1,2,3]:#testing
					auto_accelerate(self)

			elif press_key_id == 112:#p
				if self.current_mode == 0 and not self.seal_on and not self.finish_auto:
					if self.display_pausing == 1: #and '\'r\'' not in self.prompt_label.text:
						auto_pause(self)
						# cancel_events(self)
						# # s = '' 
						# # for l in self.displaying_character_labels[:self.current_char_id+1]:
						# # 	s += l.text
						# s = self.current_line[:self.current_char_id]#testing
						# print('pausing s:',s)
						# auto_prompt(self,'r',{'x':.2,'y':.3},instance=self, prompt=True,pre_info='讓我冷靜兩秒鐘...',post_info='再次面對人生')
						# Clock.schedule_once(partial(pause,self),1.2) 				

					#elif self.display_pausing == 2:
			elif press_key_id == 114:#r
				if self.current_mode == 0 and not self.seal_on and not self.finish_auto:
					if self.display_pausing == 2:  #and '\'r\'' in self.prompt_label.text:
						auto_continue(self)
						# print('Restart the auto dialog')
						# self.remove_widget(self.prompt_label)
						# s = self.current_line[self.current_char_id+1:]
						# #先跑完該句剩下的
						# s_time,c_time,n_time = read_velocity_config()
						# res_time = display_character_labels(self,s,s_time,n_time,c_time,restart_id=self.current_char_id+1)
						# #再重新開始播放動畫
						# self.auto_dialog = self.auto_dialog[self.auto_line_id+1:]
						# Clock.schedule_once(partial(auto_play_dialog,self,self.auto_dialog),res_time)#self.display_pausing = 1
						
						#self.display_pausing = 1
			#for testing
				if self.current_mode == 1:	
					self.current_mode = 3

			elif press_key_id == 101:#e: 
				if self.current_mode == 1:
					GM.ready_to_ending()

			elif press_key_id == 100:#d: 
				self.dialog_view ^= 1

			elif press_key_id == 115:#s
				if self.current_mode == 0 and not self.seal_on and not self.finish_auto:
					self.clear_text_on_screen()
					self.finish_auto = True

			elif  press_key_id == 114:#r:
				if self.current_mode == 1:	
					if self.item_view == 1: 
						self.reload_item_list = True

			elif  press_key_id == 109:#m:
				if self.current_mode == 1:
					self.complete_chapter = True
			elif  press_key_id == 110:#n:
				if self.current_mode == 1:
					if self.item_view == 0: 
						self.next_round()

			# elif press_key_id in [274,273]:
			# 	# if self.cur_unsafed:
			# 	# 	self.testing_modify_object_size(press_key_id)
			# 	if self.current_mode == 1: 
			# 		pass
			return True

	def map_objects_allocator(self, action,*args):
		if action not in ['allocate','deallocate','reallocate']:
			raise ValueError(f'Action:{action} is not supported')
		print('[*]map_objects_allocator action:',action)
		if action != 'allocate':
			print('deallocate!')
			for MapObject in self.mapobjects_register:
				self.remove_widget(MapObject)
			self.mapobjects_register = []	
		if action != 'deallocate':
			if self.item_view == 0:
				print('item_view closed, allocate!')
				print('self.objects_allocation[self.current_map_id]:',self.objects_allocation[self.current_map_id])
				for MapObject in self.objects_allocation[self.current_map_id]:#2D-list
					print('MapObject info:',MapObject.object_id,GM.object_table[str(MapObject.object_id)] ,MapObject.map_name,MapObject.pos_hint,MapObject.size_hint)
					self.mapobjects_register.append(MapObject)
					self.add_widget(MapObject)

	def map_NPCs_allocator(self, action):
		if action not in ['allocate','deallocate','reallocate']:
			raise ValueError(f'Action:{action} is not supported')
		print('[*]map_NPCs_allocator action:',action)

		if action != 'allocate':
			print('deallocate NPCs!')
			for npc in self.mapNPC_register:
				self.remove_widget(npc)
			self.mapNPC_register = []	
		if action != 'deallocate':
			print('self.NPCs_allocation[self.current_map_id]:',self.NPCs_allocation[self.current_map_id],'self.current_map_id:',self.current_map_id)
			for npc in self.NPCs_allocation[self.current_map_id]:
				print('npc info:',npc.text,npc.dialog)
				self.mapNPC_register.append(npc)
				self.add_widget(npc)

	def get_item_from_NPC(self,item_name):
		GM.players[self.current_player_id].get_item(GM.name_to_id_table[item_name])
		print('Get item from NPC:',GM.players[self.current_player_id].item_list)


	def exploring_maps(self, press_key_id):
		
		print('[*] exploring maps')
		num = len(self.chapter_maps)

		if press_key_id==276:
			print ("key action left")
			if self.current_map_id <= 0:
				self.current_map_id = num - 1			
			else:
				self.current_map_id -= 1				
		elif press_key_id==275:
			print ("key action right")
			if self.current_map_id >= num - 1:
				self.current_map_id = 0
			else:
				self.current_map_id += 1

		if self.chapter_maps[self.current_map_id].split('/')[-1].split('.')[0] in self.banned_map_list:
			print('繼續輪轉!')

			self.exploring_maps(press_key_id)		
	def generate_item_tag(self):
		print("Enter function: generate_item_tag")
		self.item_tag = Image(pos_hint={'x':.94,'y':.70},size_hint=(.06,.15),source='res/images/itemtag.png',allow_stretch=True,keep_ratio=False)#ImageButton(pos_hint={'x':.97,'y':.77},size_hint=(.03,.08),source='res/images/itemtag.png',callback=self.display_itemframe,allow_stretch=True,keep_ratio=False)
		self.add_widget(self.item_tag)

	def display_itemframe(self,*args):
		print('Enter function: display_itemframe')
		self.clear_text_on_screen()
		self.remove_widget(self.item_tag)
		if self.itemframe not in self.children: #for exceptions
			self.add_widget(self.itemframe)
		else:
			print('[*]Exceptions: self.itemframe is already added')

		self.try_open_dialog_view()	
		self.item_box_canvas_controller('show')
		self.item_tag = Image(pos_hint={'x':.74,'y':.70},size_hint=(.06,.15),source='res/images/itemtag.png',allow_stretch=True,keep_ratio=False)

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
			print('item_box_canvas_controller show')
			self.canvas.remove_group('cap')

			self.canvas_under_item_images()

			#dynamic canvas
			if direction is not None: #choosing in itemframe
				self.itemframe.switching_frame_focus(self,direction)
			else: #just open itemframe
				for i in reversed(range(self.itemframe.count)):
					item = self.itemframe.item_images[self.itemframe.cyclic[i]]
					print('add item source:',item.source)
					if item not in self.children:
						self.add_widget(item)		
					else:
						print(f'[*]Exception: item:{item} is already in the screen')
				if self.itemframe.count > 0:
					self.itemframe.focusing_frame_id = self.itemframe.cyclic[0]#->auto_focus->auto_focus_item->dragging generate
				else:
					self.itemframe.focusing_frame_id = -1

			self.canvas_on_item_images()
			#select button

		elif action == 'hide':
			
			self.canvas.remove_group('cap')
			self.itemframe.focusing_frame_id = -1 #-> focusing_object_id = -1 (remove_widget of itemframe.item_images)
			self.canvas.remove_group('itemicon') 

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
		self.canvas.add(Triangle(points=(.65*global_w,.475*global_h,.8*global_w,.475*global_h,.8*global_w,.5*global_h),group='cap'))

	def canvas_on_item_images(self):
		#box
		self.canvas.add(Color(rgba=(0,182/255,1,1),group='cap'))#source='res/images/itemframe.png',
		self.canvas.add(Rectangle(pos=(.65*global_w,.225*global_h),size=(.2*global_w,.25*global_h),group='cap'))
		self.canvas.add(Color(rgba=(0,100/255,.7,1),group='cap'))
		self.canvas.add(Quad(points=(.85*global_w,.225*global_h,.85*global_w,.475*global_h,global_w,.5*global_h,global_w,.25*global_h),group='cap'))


	def exploring_dialog(self, press_key_id):
			if press_key_id==276:
				print ("key action left")
				self.last_dialog()
			elif press_key_id==275:
				print ("key action right")
				self.next_dialog()
			print('self.manual_node.text_line:',self.manual_node.text_line)	#為何都會自動消失
	
	def next_dialog(self,*args):
		table = self.plot_scenes_table
		print('test table:',table)
		#for i in table.keys():
		i = self.switch_id
		if i < len(table.keys()):
			print(f'table[{i}][\'line\']:',table[str(i)]['line'])
			print('self.manual_node.text_line:',self.manual_node.text_line)
			if len(table[str(i)]['line'].split(':')) > 1:
				table_line =  table[str(i)]['line'].split(':')[1]
			else:
				table_line = table[str(i)]['line']
			if table_line == self.manual_node.text_line.strip('\n'):
				print('Switch bg to:',table[str(i)]['source'])
				#bg = Rectangle(source=table[str(i)]['source'], pos=(0,0), size=(self.w,self.h),group='bg')
				self.bg_widget.load_bg(table[str(i)]['source'])
				self.map_objects_allocator('deallocate')
				self.switch_id += 1

		if self.manual_node.type != 'tail':
			self.clear_text_on_screen()
			node = self.manual_node = self.manual_node.get_next()
			print('self.manual_node.text_line:',self.manual_node.text_line)
			self.lastline_time = line_display_scheduler(self,node.text_line,False,special_char_time,next_line_time,common_char_time,name=node.speaker)
		else:
			#prompt to next chapter, end round
			auto_prompt(self,'Enter',{'x':.2,'y':.3},instance=self, prompt=True,pre_info='過往妳我的緣分暫告一段落...',post_info='接著 是另外兩行人生的交錯...')

	def last_dialog(self,*args):		
		if self.manual_node.type != 'head':
			self.clear_text_on_screen()
			node = self.manual_node = self.manual_node.get_last()
			self.lastline_time = line_display_scheduler(self,node.text_line,False,special_char_time,next_line_time,common_char_time,name=node.speaker)

	#TODO: 計時器功能
	def enter_puzzle_mode(self, object_id, behavior_type):
		self.probing = False
		self.current_mode = 2
		self.canvas.add(Color(rgba=(.2,.2,.2,.2),group='puzzle_mode'))
		self.canvas.add(Rectangle(pos=self.pos,size=self.size,group='puzzle_mode'))
		item = GM.object_table[str(object_id)]
		print('puzzle_mode item:',item)


		if behavior_type != 'puzzle':
			self.try_open_item_view()
		self.clear_text_on_screen()
		print('item[\'description\']:',item['description'])
		spent_time = line_display_scheduler(self,item['description'],False,special_char_time,next_line_time,common_char_time)

		self.behavior_type = behavior_type
		if behavior_type == 'puzzle':
			self.puzzle_handler(item)
		elif behavior_type == 'lock': 
			self.lock_handler(item)
		elif behavior_type == 'synthesis': 
			self.synthesis_handler(item)
		#Debug: puzzle顯示被使用的物件敘述

	def puzzle_handler(self, item):#目前只有密碼鎖一種
		self.puzzle_name = item['name']
		self.puzzle_content = GM.puzzle_table[self.puzzle_name]
		self.answer_code =  self.puzzle_content['input']#[0,7,3,0]	
		build_CodedLock(self,item)

	def puzzle_select_number(self,press_key_id):

		if press_key_id == 273:
			self.cur_code[self.code_id] = num_up[self.cur_code[self.code_id]]
		elif press_key_id == 274:
			self.cur_code[self.code_id] = num_down[self.cur_code[self.code_id]]
		self.code_labels[self.code_id].text = str(self.cur_code[self.code_id])

		if self.cur_code == self.answer_code:
			self.puzzling = False

			quit_text = '解碼成功...'
			if self.puzzle_content['output_item'] is not None:
				print('解碼成功...獲得新道具!')
				quit_text += '獲得新道具! '

				output_id = GM.name_to_id_table[self.puzzle_content['output_item']]
				GM.players[self.current_player_id].get_item(output_id)#->auto_reload_item_list->auto_gen_items	
			if self.puzzle_content['new_scene'] is not None:
				print('解碼成功...解鎖新場景!')
				quit_text += '解鎖新場景! '
				name = self.puzzle_content['new_scene']
				GM.Chapters[self.current_player_id][self.current_chapter].unlock_new_map(name)
				self.current_map_id = len(self.chapter_maps) - 1 #unlock and go to new scene
			if self.puzzle_content['trigger']:
				print('解碼成功...觸發劇情!')
				quit_text += '觸發劇情!\n'
				self.quit_puzzle_mode(text=quit_text,turn_mode = 3)
			else:
				quit_text += '\n'
				self.quit_puzzle_mode(text=quit_text)

	def synthesis_handler(self, item):
		material = item['name']  
		synthesis_content = GM.synthesis_table[material]
		expected_input = synthesis_content['input']

		synthesis_canvas(self,item,0)
		if self.itemframe.count > 0:
			self.global_mouse_event = Clock.schedule_interval(global_mouse, 0.1)
			self.synthesis_event = Clock.schedule_interval(partial(self.material_item_judge,item,synthesis_content), 0.1)

	def material_item_judge(self,item,synthesis_content,*args):
		def try_synthesis(screen,item,expected_input,dragging_object_id,*args):
			if self.judgable:
				self.judgable = False
			else:
				return
			if GM.object_table[str(dragging_object_id)]['name'] == expected_input:
				screen.synthesis_event.cancel()
				screen.global_mouse_event.cancel()
				synthesizer_id = GM.name_to_id_table[item['name']]
				GM.players[screen.current_player_id].spend_item(synthesizer_id)
				GM.players[screen.current_player_id].spend_item(dragging_object_id)
				print('合成成功...獲得新道具!')
				screen.quit_puzzle_mode(text='合成成功...獲得新道具!\n')
				output_id = GM.name_to_id_table[synthesis_content['output']]#WARNING: name_to_id可能重複
				Clock.schedule_once(partial(synthesis_canvas,self,item,2,GM.object_table[str(output_id)]['source']),.5) 
				GM.players[screen.current_player_id].get_item(output_id)

			else:
				print('合成失敗!')
				screen.clear_text_on_screen()
				spent_time = line_display_scheduler(screen,'合成失敗...\n',False,special_char_time,next_line_time,common_char_time)
				Clock.schedule_once(partial(screen.dragging.reset,screen,2),spent_time+1.5) 
				Clock.schedule_once(screen.set_judgable,spent_time+1.6) #testing		
				self.canvas.remove_group('synthesis1')
				self.hp_per_round -= 1
				#screen.hp_per_round -= 1

		expected_input = synthesis_content['input']
		dragging_object_id = self.itemframe.item_list[self.itemframe.cyclic[0]] 
		if E2_distance(self.dragging.stopped_pos,(global_x,global_y))< 10 and self.mouse_in_range({'x':.34,'y':.6} ,(.12,.2)):
			print('嘗試合成')
			self.remove_widget(self.dragging)
			Clock.schedule_once(partial(synthesis_canvas,self,item,1,self.dragging.source),.1)
			Clock.schedule_once(partial(try_synthesis,self,item,expected_input,dragging_object_id),1.1)
		elif not self.mouse_in_range({'x':.34,'y':.6} ,(.12,.2)) and self.dragging.free == 1 :

			print('合成超出範圍，返回原位')		
			self.dragging.reset(self,2)

	def lock_handler(self, item):
		lock_name = item['name']
		lock_content = GM.unlock_table[lock_name]
		expected_input = lock_content['input_item']
		judge_pos_hint, judge_size_hint = {'x':.35,'y':((global_h-.3*global_w)/2)/global_h},(.3,.3*global_w/global_h)
		if item['source'] is not None:
			print('item[\'source\']:',item['source'])
			self.canvas.add(Color(rgba=(1,1,1,1),group='lock'))
			self.canvas.add(Rectangle(source=item['source'],pos=(.35*global_w,(global_h-.3*global_w)/2),size=(.3*global_w,.3*global_w),group='lock'))
		else:
			judge_pos_hint, judge_size_hint = {'x':item['pos_hint'][0],'y':item['pos_hint'][1]}, item['size_hint']
		print('judge_pos_hint, judge_size_hint:',judge_pos_hint, judge_size_hint)
		if self.itemframe.count > 0:
			self.global_mouse_event = Clock.schedule_interval(global_mouse, 0.1)
			self.lock_event = Clock.schedule_interval(partial(self.key_item_judge,lock_content,judge_pos_hint, judge_size_hint), 0.1)

	def key_item_judge(self, lock_content, judge_pos_hint, judge_size_hint, *args):
		expected_input = lock_content['input_item']
		dragging_object_id = self.itemframe.item_list[self.itemframe.cyclic[0]] 
		if E2_distance(self.dragging.stopped_pos,(global_x,global_y))< 10 and self.mouse_in_range(judge_pos_hint, judge_size_hint):
			if GM.object_table[str(dragging_object_id)]['name'] == expected_input and self.judgable:#passed the lock
				self.judgable = False
				self.lock_event.cancel()
				self.global_mouse_event.cancel()
				GM.players[self.current_player_id].spend_item(dragging_object_id)#->auto_reload_item_list->auto_gen_items	
				#lock_output: output item, new scene, trigger
				quit_text = '開鎖成功...'
				if lock_content['output_item'] is not None:
					print('開鎖成功...獲得新道具!')
					quit_text += '獲得新道具! '
					if isinstance(lock_content['output_item'],list):
						for out in lock_content['output_item']:
							output_id = GM.name_to_id_table[out]
							GM.players[self.current_player_id].get_item(output_id)
					else:
						output_id = GM.name_to_id_table[lock_content['output_item']]
						GM.players[self.current_player_id].get_item(output_id)#->auto_reload_item_list->auto_gen_items	
				if lock_content['new_scene'] is not None:
					print('開鎖成功...解鎖新場景!')
					quit_text += '解鎖新場景! '
					name = lock_content['new_scene'].split('\'')[1]
					GM.Chapters[self.current_player_id][self.current_chapter].unlock_new_map(name)
					self.current_map_id = len(self.chapter_maps) - 1 #unlock and go to new scene
				if lock_content['trigger']:
					print('開鎖成功...觸發劇情!')
					quit_text += '觸發劇情!\n'
					self.quit_puzzle_mode(text=quit_text,turn_mode = 3)
				else:
					quit_text += '\n'
					self.quit_puzzle_mode(text=quit_text)						
			elif self.judgable:
				self.judgable = False
				print('開鎖失敗!')
				self.clear_text_on_screen()
				self.try_open_dialog_view()
				spent_time = line_display_scheduler(self,'開鎖失敗...\n',False,special_char_time,next_line_time,common_char_time)
				Clock.schedule_once(partial(self.dragging.reset,self,2),spent_time+1) 	
				Clock.schedule_once(self.set_judgable,spent_time+1.1)
				self.hp_per_round -= 1
		elif not self.mouse_in_range(judge_pos_hint, judge_size_hint) and self.dragging.free == 1:
			print('開鎖超出範圍，返回原位')		
			self.dragging.reset(self,2)

	def mouse_in_range(self,pos_hint,size_hint):
		xh = global_x/global_w
		yh = global_y/global_h
		if xh >= pos_hint['x'] and xh <= pos_hint['x']+size_hint[0] and \
		yh >= pos_hint['y']	and yh <= pos_hint['y']+size_hint[1]:
			print('mouse in range')
			self.in_judge_range = True
			return True
		else:
			print('mouse not in range')
			self.in_judge_range = False
			return False

	def quit_puzzle_mode(self,text='再試試看吧...',turn_mode=1):

		def systhesis_canvas_clear(screen,*args):
			screen.canvas.remove_group('synthesis')
			screen.canvas.remove_group('synthesis1')
			screen.canvas.remove_group('synthesis2')			
		self.canvas.remove_group('puzzle_mode')
		if self.behavior_type == 'puzzle':
			self.canvas.remove_group('puzzle')
			clear_CodedLock(self)#only for codedlock 
		elif self.behavior_type == 'lock':
			try:
				self.lock_event.cancel()
				self.global_mouse_event.cancel()
			except:
				pass
			self.canvas.remove_group('lock')	
		elif self.behavior_type == 'synthesis':
			print('quit synthesis')
			try:
				self.synthesis_event.cancel()
				self.global_mouse_event.cancel()		
			except:
				pass
			Clock.schedule_once(partial(systhesis_canvas_clear,self),1.2)
			print('stage == 2 removed')
		self.dialog_view = 1
		self.clear_text_on_screen()
		spent_time = line_display_scheduler(self,text,False,special_char_time,next_line_time,common_char_time)
		Clock.schedule_once(self.set_judgable,spent_time)
		self.remove_widget(self.dragging)

		print('puzzle mode turn to:',turn_mode)
		if turn_mode == 1:
			if self.item_view == 1:
				Clock.schedule_once(self.try_close_item_view,spent_time+.1)

			self.current_mode = turn_mode 

		elif turn_mode == 3:
			print('self.current_mode:',self.current_mode )	
			auto_prompt(self,'q',{'x':.2,'y':.3},instance=self, prompt=True,pre_info='於是，我也墮入了回憶...\n',post_info='不再回頭')

	def on_press_item(self, btn):

		self.hp_per_round -= 1
		self.pickup_chapter_objects(btn)

		self.dialog_view = 1
		spent_time = line_display_scheduler(self,'好像撿到有用的道具了呦\n',False,special_char_time,next_line_time,common_char_time)
		self.delay_hide_dialogframe(spent_time)

	def pickup_chapter_objects(self,btn,action='to_bag'):
		# picked_item = None
		# for MapObject in self.objects_allocation[self.current_map_id]:
		# 	if MapObject.object_id == object_id:
		# 		picked_item = MapObject
		# 		print('picked_item:',picked_item.object_id)
		# 		break

		print('self.objects_allocation[self.current_map_id]:',self.objects_allocation[self.current_map_id])
		#self.objects_allocation[self.current_map_id].remove(picked_item)
		#self.chapter_info.chapter_objects_of_maps[self.current_map_id].remove(picked_item)
		self.chapter_info.remove_objects_on_map(self.current_map_id,btn)
		print('after self.objects_allocation[self.current_map_id]:',self.objects_allocation[self.current_map_id])
		if action == 'to_bag':
			GM.players[self.current_player_id].get_item(btn.object_id)
		#self.remove_widget(btn) 

	def on_press_puzzle(self, btn):
		self.enter_puzzle_mode(btn.object_id, 'puzzle')	

	def on_press_lock(self,btn):
		self.enter_puzzle_mode(btn.object_id, 'lock')	

	def on_press_synthesis(self,btn):
		self.enter_puzzle_mode(btn.object_id, 'synthesis')	

	def on_press_trigger(self,btn):
		self.probing = False
		self.current_mode = 3

	def on_press_clue(self, btn):
		self.hp_per_round -= 1
		self.dialog_view = 1
		text_line = btn.object_content['description']
		spent_time = line_display_scheduler(self,text_line,False,special_char_time,next_line_time,common_char_time)
		self.delay_hide_dialogframe(.5+spent_time)

		item_name = text_line[text_line.find('(')+1:text_line.find(')')].split(':')[1]
		print('獲得敘述中道具:',btn,item_name)
		item_id = GM.name_to_id_table[item_name]
		GM.players[self.current_player_id].get_item(item_id)
		self.pickup_chapter_objects(btn,action='discard')	

	def on_press_switching(self,btn):
		self.probing = False

		new_scene_name = btn.object_content['description'] 
		print('new_scene_name:',new_scene_name)
		print('self.chapter_maps:',self.chapter_maps)
		for i,img in enumerate(self.chapter_maps):
			if new_scene_name in img:
				self.current_map_id = i

	def on_press_nothing(self, btn):
		self.hp_per_round -= 1
		self.dialog_view = 1
		text_line = btn.object_content['description']
		if len(text_line) == 0:
			text_line = '不太清楚這有什麼用...\n'
		spent_time = line_display_scheduler(self,text_line,False,special_char_time,next_line_time,common_char_time)
		self.delay_hide_dialogframe(spent_time)

	def delay_hide_dialogframe(self, delay_time):
		print('delay hide dialogframe')
		Clock.schedule_once(self.try_close_dialog_view,delay_time+.1)
		self.clear_text_on_screen(delay_time=delay_time)
		def probing_free(screen,*args):
			self.probing = False
		Clock.schedule_once(partial(probing_free,self),delay_time+.2)

	def set_judgable(self,*args):
		print('[*] set judgable')
		if not self.judgable:
			self.judgable = True

	def try_close_dialog_view(self,*args):
		if self.dialog_view == 1:
			self.dialog_view = 0	

	def try_close_item_view(self,*args):
		if self.item_view == 1:
			self.item_view = 0

	def try_open_dialog_view(self,*args):
		if self.dialog_view == 0:
			self.dialog_view = 1	

	def try_open_item_view(self,*args):
		#self.try_close_dialog_view()
		if self.item_view == 0:
			self.item_view = 1

	#TODO: 移到dialog_utils
	def clear_text_on_screen(self,uncontinuous=True,delay_time=0,*args):
		print('[*]clear_text_on_screen!!')

		#delay at here
		if delay_time > 0:
			Clock.schedule_once(partial(cancel_events,self), delay_time) 
			Clock.schedule_once(partial(clear_displayed_text,self,self.displaying_character_labels), delay_time)
		else:
			cancel_events(self)
			clear_displayed_text(self,self.displaying_character_labels)
		
		if uncontinuous:
			self.dialog_events = []	
		self.text_cleared = True	

	def to_epo_screen(self,*args):
		if self.current_mode == 1:
			self.manager.get_screen('epo').load_personal_ePo(self.current_player_id,self.current_chapter)
			self.manager.current = 'epo'

	#for testing: 	
	def to_game_screen(self,*args):
		if self.current_mode == 1:
			subgames_id = 0#decided by story
			self.manager.current = 'subgames_manager'
			if not self.manager.get_screen('subgames_manager').initialized:
				self.manager.get_screen('subgames_manager').init_all_subgames()
			self.manager.get_screen('subgames_manager').start_subgame_id(subgames_id)		

	def auto_golden_player(self,instance,golden_id):#直接完成遊戲的通關密碼
		print('[*] get golden_id:',golden_id)
		if golden_id >= len(self.golden_password):
			auto_prompt(self,'g',{'x':.2,'y':.3},instance=self, prompt=True,pre_info='你，也像我一樣看透人生了嗎\n',post_info='坦然接受，無論結局為何...')

	def auto_cheat_chapter(self,instance,cheat_chapter_id):
		print('[*] get cheat_chapter_id:',cheat_chapter_id)
		if cheat_chapter_id >= len(self.cheat_chapter_password):
			auto_prompt(self,'q',{'x':.2,'y':.3},instance=self, prompt=True,pre_info='於是，我不惜一切代價也要墮入回憶...\n',post_info='喚醒早已深沉的一切')

	def load_game(self):
		GM.load_game(self)

	def auto_save_game(self,*args):
		if not self.loading:
			GM.save_game(self)		
			#TODO: 按照修改的資料種類傳參數進去改寫部分紀錄檔即可

	@staticmethod
	def exit_game():
		exit()

	# #for testing: drag objects to map location and save
	# def testing_objects_path_init(self):#
	# 	import shutil
	# 	self.testing_objects = []
	# 	self.testing_objects_id = -1
	# 	dir_path = 'res/images/unlocated_mapobjects/' 
	# 	paint_path = 'res/images/handpainting/'

	# 	for origin in os.listdir(dir_path):
	# 		os.remove(os.path.join(dir_path,origin))
	# 	#
	# 	allocated_data = {}
	# 	if os.path.isfile('res/allocate_all_objects_table.json'):
	# 		f = open('res/allocate_all_objects_table.json','r')
	# 		allocated_data = json.load(f)
	# 		print('exist allocated_data before testing:',allocated_data)
	# 		f.close()

	# 	#load unlocated mapobjects
	# 	for key,item in GM.object_table.items():
	# 		for img_name in os.listdir(paint_path):
	# 			if item['on_map'] and item['source'] is not None and item['name'] in img_name and item['name'] not in allocated_data.keys():
	# 				shutil.copy(os.path.join(paint_path,img_name),dir_path)
	# 				print(f'testing copy key:{key},item:{item} to unlocated_mapobjects dir')
					
	# 	#generate testing objects			
	# 	files = os.listdir(dir_path)
	# 	for f in files:
	# 		if '.jpg' in f or '.png' in f:
	# 			fulldir_path = os.path.join(dir_path,f)
	# 			if os.path.isfile(fulldir_path):
	#  				self.testing_objects.append(fulldir_path)	
	# 	print('testing objects:',self.testing_objects)		
	# 	self.cur_unsafed = False	

	# #for testing: drag objects to map location and save
	# def testing_set_objects_pos(self):
	# 	if self.testing_objects_id > len(self.testing_objects)-2:
	# 		return 
	# 	else:
	# 		self.testing_objects_id += 1
	# 	source=self.testing_objects[self.testing_objects_id]
	# 	print('testing source:',source)
	# 	self.cur_testing_dragitem = FreeDraggableItem(pos=(0,0),size=(100,100),source=source,size_hint=(None,None))
	# 	self.add_widget(self.cur_testing_dragitem)
	# 	self.cur_unsafed = True

	# #for testing: drag objects to map location and save	
	# def testing_save_object_pos(self):
	# 	data = {}
	# 	if os.path.isfile('res/allocate_all_objects_table.json'):
	# 		f = open('res/allocate_all_objects_table.json','r')
	# 		data = json.load(f)
	# 		print('exist data:',data)
	# 		f.close()
	# 	pos_hint = self.cur_testing_dragitem.stopped_pos_hint
	# 	size_hint = (self.cur_testing_dragitem.size[0]/global_w,self.cur_testing_dragitem.size[1]/global_h)
	# 	source = self.testing_objects[self.testing_objects_id].replace('unlocated_mapobjects','handpainting')
	# 	os.remove(self.testing_objects[self.testing_objects_id])

	# 	#write: player_id,chapter_id,mapid,object_pos_hint, source	
	# 	item_name = source.split('/')[-1].split('.')[0]

	# 	data[item_name] = {'pos_hint':pos_hint,'size_hint':size_hint,'source':source}
	# 	print(f'Save data[{item_name}]: {data[item_name]}!')
	# 	with open('res/allocate_all_objects_table.json','w') as f:	
	# 		json.dump(data, f)
	# 	self.remove_widget(self.cur_testing_dragitem)
	# 	#f.write(f'player_id:{self.current_player_id},chapter_id:{self.current_chapter},mapid:{self.current_map_id},object_pos_hint:{pos_hint},object_size_hint:{size_hint},source:{source}\n')
	# 	#f.close()
	# 	self.cur_unsafed = False

	# #for testing: 
	# def testing_modify_object_size(self, press_key_id):
	# 	if press_key_id == 274:
	# 		self.cur_testing_dragitem.size[0] -= 10
	# 		self.cur_testing_dragitem.size[1] -= 10
	# 	elif press_key_id == 273:
	# 		self.cur_testing_dragitem.size[0] += 10
	# 		self.cur_testing_dragitem.size[1] += 10
	
	# #for testing: 
	# def testing_embeded_object_marker(self):
	# 	pass

def global_mouse(*args):
	global global_x,global_y
	if OS == "Darwin": #Macbook
		global_x, global_y = pygame.mouse.get_pos()#Bugs in Windows
		global_y = global_h - global_y
	elif OS == "Windows":#Windows
		_,_,(global_x, global_y) = win32gui.GetCursorInfo()
		global_y = global_h - global_y
