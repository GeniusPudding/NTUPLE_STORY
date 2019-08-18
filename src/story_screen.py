###################################################
# Main screen of this game                        #
###################################################
from game_manager import *

GM = GameManagerScreen()
global_x = 0
global_y = 0

class ItemFrame(FloatLayout):#TODO: 立體版UI之外提供切換成平面模式的功能

	parent_w = NumericProperty()
	parent_h = NumericProperty()
	focusing_frame_id = NumericProperty(-1)
	item_list = ListProperty([])
	#offset = ListProperty((0,0))
	switchable = BooleanProperty(True)
	playing_anim_num = NumericProperty()
	def __init__(self,screen,**kwargs):
		super(ItemFrame, self).__init__(**kwargs)
		print(f"init itemframe global_w:{global_w},global_h:{global_h},self.size:{self.size},self.parent={self.parent}:")

		self.parent_w = global_w#parent_w
		self.parent_h = global_h#parent_h
		self.infoFrame = Widget()
		self.item_name = Widget()
		self.infoContent = Widget()
		self.screen = screen
		self.bind(item_list=self.auto_gen_items)#after auto_reload_item_list called
		self.bind(focusing_frame_id=self.auto_focus)

		# print("self.x,self.y:",self.x,self.y)
		self.front_pos = (.75*global_w,.4*global_h)
		self.back_pos = (.85*global_w,.45*global_h)#for animations

		self.offset = (0,0)
		self.count = 0
		self.item_size = (.04*global_w,.06*global_h)
		self.info_size_x, self.info_size_y = .12*global_w,.18*global_h
		self.cyclic = {}
		self.item_images = []
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
		#print('GM.object_table:',GM.object_table)
		d_len = min(.15*global_w,.2*global_h)
	

		#DEBUG:有時會無法加回主畫面
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
		screen.clear_text_on_screen()	#DEBUG
		if focusing_frame_id >= 0:	
			
			#screen.remove_widget(self.item_name)
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
		self.item_name = Label(text= GM.object_table[str(object_id)]['name'],pos_hint={'x':0,'y':.2},color=(.7,1,.4,1),font_size=30,size_hint=(.1,.07),font_name= 'res/HuaKangTiFan-CuTi-1.otf')
		screen.add_widget(self.item_name)
	def display_item_info(self,object_id,screen):
		print('auto_display_item_info object_id:',object_id)
		text_line = GM.object_table[str(object_id)]['description']
		if len(text_line) == 0:
			text_line = '不明道具...不知道可以用來做什麼'
		print('text_line:',text_line)
		spent_time = line_display_scheduler(screen,text_line,False,.2,.5,.15)
		# Clock.schedule_once(screen.clear_text_on_screen,.2+spent_time)
		#screen.clear_text_on_screen(delay_time=.2+spent_time)
			
	def switching_frame_focus(self,screen,press_key_id):#handle the cyclic animation
		#DEBUG: 同步還沒做，切換太快自動字幕會來不及放出
		self.switchable = False
		if screen.item_view == 0:
			print('dialogframe closed too fast!')
			screen.item_view = 1
		n = self.playing_anim_num = self.count #determined by the number of animations
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

		self.switchable = True


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
		# if touch is None:#TODO: controlable MotionEvent
		# 	touch = MotionEvent(device=None,id='mouse2',profile=['pos'],is_touch=True)#,)

		if len(types) == 1:#'item' only, 
			
			if touch is not None:
				print("拖曳普通道具!")
				screen.add_widget(screen.dragging)
				screen.dragging.on_touch_down(touch)
			else:
				print("普通道具，無法單獨使用!")#DEBUG:clear
				screen.clear_text_on_screen()
				spent_time = line_display_scheduler(screen,'普通道具，無法單獨使用!',False,special_char_time,next_line_time,common_char_time)
				#Clock.schedule_once(screen.clear_text_on_screen,spent_time+.5)
				#screen.clear_text_on_screen(delay_time=spent_time+.5)
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
		#for testing
		print('itemframe touch.profile:',touch.profile,'touch.id:',touch.id,'touch.pos:',touch.pos)
		if self.parent is not None and self.focusing_frame_id >= 0 and self.item_images[self.focusing_frame_id].collide_point(*touch.pos) and self.count > 0:
			object_id = self.item_list[self.focusing_frame_id]
			screen = self.parent
			self.use_item(screen,object_id,touch)




class StoryScreen(Screen):#TODO: 如何扣掉Windows電腦中screen size的上下面, 注意image檔案拉扯問題
	#TODO: EXCEPTIONS!!!
	#TODO: ban右鍵控制
	
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
	puzzling = BooleanProperty(False)
	current_scene = StringProperty('')
	behavior_type = StringProperty('')
	probing = BooleanProperty(False)
	loading = BooleanProperty(True) 
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
		self.bind(hp_per_round=self.auto_hp_canvas)
		#self.bind(hp_per_round=self.auto_save_game)
		self.bind(current_speaker_name=partial(auto_display_speaker,self))
		self.bind(current_map_id=self.auto_switch_maps)
		#self.bind(current_map_id=self.auto_save_game)#DEBUG: 無法存到
		#self.bind(current_player_chapter=self.auto_reload_chapter_info)
		self.bind(chapter_info=self.auto_load_chapter_info_contents)
		self.bind(dialog_view=self.auto_dialog_view)
		self.bind(item_view=self.auto_item_view)
		self.bind(complete_chapter=self.auto_end_chapter)
		self.bind(seal_on=self.auto_seal)
		self.bind(current_mode=self.auto_switch_mode)
		#self.bind(current_mode=self.auto_save_game)
		self.bind(finish_auto=partial(auto_prompt,self,'Enter',{'x':.25,'y':.4}))
		self.bind(finish_auto=self.auto_start_chapter)
		self.bind(reload_item_list=self.auto_reload_item_list)
		self.bind(focusing_object_id=self.auto_focus_item)
		Window.bind(on_key_down=self.key_action)
		Window.bind(on_key_up=self.key_release)
		self.hp_widgets = []
		self.displaying_character_labels = []
		self.lock = Image()
		self.chapter_title = Label()
		self.mapobjects_register = []
		self.objects_allocation = [[]]
		#self.nametag = Label()#(Image(),Label())
		sub_size = max(self.w*self.button_width*.6,self.h*self.button_height*.8)
		self.subgame_button = ImageButton(callback=self.to_game_screen,source='res/images/testing/subgame_icon.png',pos_hint={'x':self.dialogframe_width+self.button_width-sub_size/self.w,'y':self.dialogframe_height},size_hint=(sub_size/self.w,sub_size/self.h))


		self.bg_widget = BG_widget(parent =self)
		self.add_widget(self.bg_widget) 

		self.next_round()
		#self.load_game() #testing auto load/save this game, or set a button

	#the entry of main function in each round 	
	def next_round(self,*args):
		print("Enter function: next_round")
		#<clear the last round status>: 清除前一位玩家回合狀態 	
		self.end_round = False#TODO: if true, 出現輪下一位玩家的按鈕或按鍵提示
		self.complete_chapter = False
		#for testing
		#self.remove_widget(self.subgame_button)

		#<modify game info>: 配置回合切換所需 
		self.current_player_id, self.current_chapter = GM.change_turn()#Then call auto_reload_chapter_info, and then bind auto_load_chapter_info_contents
		#陷阱!!!有先後順序 會auto_reload_chapter_info兩次 
		print("player:{}, chapter:{} ,self.size:{}".format(self.current_player_id, self.current_chapter,self.size))		
		self.auto_reload_chapter_info(self,[self.current_player_id, self.current_chapter])


		#round-binding canvas: 
		#self.hp_per_round = 1
		self.hp_per_round = 20#trigger event #auto save?

		#<chapter info part>: 透過bind auto_load_chapter_info_contents，從 chapter_info 載入所有地圖所需
		self.current_map_id = -2
		self.current_map_id = self.chapter_info.chapter_default_map #0#trigger the map loading function
		#print("self.chapter_maps[self.current_map_id]:",self.chapter_maps[self.current_map_id])
		#print('Restart test')
		#for testing, load subgame button 
		#self.add_widget(self.subgame_button)

		#for testing
		#self.testing_objects_path_init()

		#for testing
		# test1 = MapObject(screen=self, object_id=125,object_content=GM.object_table[str(125)],size_hint=(.15,.15),pos_hint={'x':.5,'y':.3})
		# test2 = MapObject(screen=self, object_id=127,object_content=GM.object_table[str(127)],size_hint=(.15,.15),pos_hint={'x':.3,'y':.3})
		# test3 = MapObject(screen=self, object_id=124,object_content=GM.object_table[str(124)],size_hint=(.15,.15),pos_hint={'x':.5,'y':.5})
		# test4 = MapObject(screen=self, object_id=6,object_content=GM.object_table[str(6)],size_hint=(.15,.15),pos_hint={'x':.3,'y':.5})
		# test5 = MapObject(screen=self, object_id=58,object_content=GM.object_table[str(58)],size_hint=(.15,.15),pos_hint={'x':.1,'y':.3})
		# test6 = MapObject(screen=self, object_id=66,object_content=GM.object_table[str(66)],size_hint=(.15,.15),pos_hint={'x':.1,'y':.5})
		# self.remove_widget(test1)#lock 
		# self.remove_widget(test2)#lock input item  
		# self.remove_widget(test3)#nothing
		# self.remove_widget(test4)#switching
		# self.remove_widget(test5)#puzzle 木製保險櫃(關)
		# self.remove_widget(test6)#synthesis		
		# self.add_widget(test1)#lock 
		# self.add_widget(test2)#lock input item  
		# self.add_widget(test3)#nothing
		# self.add_widget(test4)#switching
		# self.add_widget(test5)#puzzle 木製保險櫃(關)
		# self.add_widget(test6)#synthesis

		#auto save
		if self.finish_auto:
			self.auto_save_game()



	def auto_switch_mode(self, instance, mode):#Entry of all stroy screen modes
		print('[*]Switch mode:', mode)
		if mode == 0:#For each chapter starts
			self.seal_on = True

		elif mode == 1:#start exploring
			Clock.schedule_once(self.try_close_dialog_view,.8)

			#start exploring mode, allocate objects on chapter's map 
			self.map_objects_allocator('reallocate')				


		elif mode == 2:#for banning some game functions in mode 1(exploring mode)
			self.item_view = 1
			#TODO配置一個小返回按鈕提示於角落，按下'b'回到mode 1

		elif mode == 3:
			if self.item_view == 1:
				self.item_view = 0#self.map_objects_allocator('deallocate')
			else:
				self.map_objects_allocator('deallocate')
			self.dialog_view = 1#DEBUG 檢查同步機制，小心被canvas上其它東西蓋到
			self.manual_node = semi_manual_play_dialog(self,self.manual_dialog)
			auto_prompt(self,'->',{'x':.25,'y':.4},instance=self, prompt=True,extra_info='For next sentence...\n')

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
		if not self.chapter_info.started:#finish_auto
			self.finish_auto = False
			self.chapter_title = self.chapter_info.chapter_title
			self.current_mode = 0
		else:
			self.current_mode = 1
		self.chapter_maps = chapter_info.chapter_maps
		self.NPCs_allocation = chapter_info.chapter_NPCs#deprecated
		self.objects_allocation = chapter_info.chapter_objects#DEBUG:疑似蓋掉原本的canvas圖片
		self.auto_dialog = self.chapter_info.chapter_pre_plot 
		self.manual_dialog = self.chapter_info.chapter_plot
		self.scenes = self.chapter_info.chapter_plot_scenes
		self.plot_scenes_table = self.chapter_info.chapter_scenes_table

		self.remove_widget(self.itemframe)
		self.itemframe = ItemFrame(screen = self,pos_hint = {'x':.8,'y':.25},size_hint = (.2,.6))#(pos_hint = {'x':.15,'y':.33},size_hint = (.85,.5))#parent_w=self.w,parent_h=self.h
		self.reload_item_list = True
		self.generate_item_tag()
		#print('chapter_info:', chapter_info,'self.itemframe:',self.itemframe)
		
		print(f'chapter_maps:{self.chapter_maps},objects_allocation:{self.objects_allocation}')#,current_dialog:{self.auto_dialog}')

	def auto_start_chapter(self, instance, finish_auto):
		if finish_auto:
			GM.start_chapter() #let self.chapter_info.started = True
			self.loading = False
			self.auto_save_game()
	def auto_end_chapter(self, instance, complete_chapter):#called when outer calls "self.complete_chapter = True"  
		if complete_chapter:#DEBUG
			print('[*]complete_chapter:', complete_chapter)#after the plot's dialog ended
			GM.change_chapter()
			#TODO: link to the plot of the chapter's ending
			
			self.next_round()
	#TODO: load story's dialog
	def auto_dialog_view(self, instance, dialog_view):
		print('[*]dialog view:', dialog_view)
		
		if dialog_view == 1:
			print("load dialog view")
			self.canvas.add(Rectangle(source='res/images/origin_dialogframe.png',pos=(0,0),size=(self.w*self.dialogframe_width,self.h*(self.dialogframe_height+.07)),group='dialogframe'))
		elif dialog_view == 0:
			print("hide dialog view")	
			self.current_speaker_name = 'N'
			#if len(self.displaying_character_labels) > 0:#dialog_events
			self.clear_text_on_screen()
			self.canvas.remove_group('dialogframe')


	def auto_item_view(self, instance, item_view):#Entry and Exit of all itemframe functions
		print('[*]item view:', item_view)#TODO: 檢查會有哪些地方需要MUTEXs or Locks去同步共享資源
		if item_view == 1:#TODO:改成另外呼叫open itemframe而非直接改item_view值
			self.map_objects_allocator('deallocate')#DEBUG
			self.display_itemframe()	
		elif item_view == 0:
			self.hide_itemframe()
			self.map_objects_allocator('allocate')

	#select the background image of this story	
	def auto_reload_chapter_info(self, instance, c_p):#do not bind "self.current_player_id, self.current_chapter = GM.change_turn()" !
		print('[*]current_player_chapter: ', c_p)
		self.chapter_info = GM.Chapters[self.current_player_id][self.current_chapter]#load chapter info at each round starts
		print("chapter_info reloaded:",self.chapter_info)
	def auto_hp_canvas(self,instance, hp):#if hp = 0, end this round
		print('[*]hp:', hp)#TODO:hp-1 動畫 
		for hp in self.hp_widgets:
			self.remove_widget(hp)
		for i in range(self.hp_per_round):#TODO: 換圖片(希望跟台大有關), 改成canvas繪圖
			hp = Image(source='res/images/testing/HP.png',pos_hint={'x':.94-.04*i,'y':.85},size_hint=(.03,.1))
			self.add_widget(hp)
			self.hp_widgets.append(hp)
		if self.hp_per_round <= 0:
			self.quit_puzzle_mode()
			#TODO:check if there is any status not be cleared
			auto_prompt(self,'Enter',{'x':.25,'y':.4},instance=self, prompt=True,extra_info='體力耗盡!\n')

			                         

	def auto_switch_maps(self,instance, current_map_id):#TODO: 清除所有畫面上部件重新載入，或是把這個功能做在切換回合時
		if current_map_id >= 0:

			print('[*]current map:', current_map_id)
			print("self.chapter_maps:",self.chapter_maps)
			#self.canvas.before.remove_group('bg')
			print("self.chapter_maps[current_map_id]:",self.chapter_maps[current_map_id])
			bg = Rectangle(source=self.chapter_maps[current_map_id], pos=(0,0), size=(self.w,self.h),group='bg')
			self.bg_widget.load_bg(bg)
			if self.item_view == 1:
				self.item_view == 0
			if self.current_mode in [1,2] :#DEBUG
				self.map_objects_allocator('reallocate')

		#TODO:
		#elif == -1: 
		#	GM.unlock_new_map(self.new_map_name) 加入解鎖新場景的物件

	def auto_reload_item_list(self,instance, reload_item_list):
		if reload_item_list:
			print('[*] auto update instance:',reload_item_list)
			print('init self.itemframe.item_list:',self.itemframe.item_list)
			self.itemframe.item_list = GM.players[self.current_player_id].item_list #->auto_gen_items
			print('after init self.itemframe.item_list:',self.itemframe.item_list)

			print('reload items:',self.itemframe.item_list)	
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
			#self.add_widget(self.dragging)
		else:
			for item in self.itemframe.item_images:
				self.remove_widget(item)	

	def key_action(self, *args):#TODO:盡量統一按鍵、做好遊戲按鍵提示介面
		if self.manager.current == 'story':	
			print('story key: ',args)
			press_key_id = args[1]#args[1]:ASCII
			press_key = args[3]
			if press_key_id in [276,275]:#<-,->

				if self.current_mode == 1:	
					if self.item_view == 0:
						if self.displaying_character_labels == [] and self.dialog_events == []:
							self.exploring_maps(press_key_id)
					elif self.item_view == 1:
						if self.itemframe.switchable and self.itemframe.playing_anim_num <= 0 and self.itemframe.count > 1:
							self.item_box_canvas_controller('show',direction=press_key_id) 
						else:
							print('Wait for item canvas finish')
				elif self.current_mode == 2:
					if not self.puzzling:
						if self.itemframe.switchable and self.itemframe.playing_anim_num <= 0:
							self.item_box_canvas_controller('show',direction=press_key_id) 
					else:		
						puzzle_move_view(self,press_key_id)

				elif self.current_mode == 3:
					self.remove_widget(self.prompt_label)	
					self.exploring_dialog(press_key_id)

			elif press_key_id in [274,273]:
				# if self.cur_unsafed:
				# 	self.testing_modify_object_size(press_key_id)
				if self.puzzling:
					puzzle_select_number(self,press_key_id)		

			elif press_key_id == 98:#b:
				if self.current_mode == 2:
					self.quit_puzzle_mode()


			elif press_key_id == 105:#i:
				if self.current_mode == 1:
					self.item_view ^= 1

			elif press_key_id == 13:#Enter
				if self.seal_on and not self.finish_auto and self.manager.current == 'story':
					print('Get ENTER to clear the seal!')
					self.seal_on = False

				elif self.current_mode == 0 and self.finish_auto:
					self.remove_widget(self.prompt_label)
					self.current_mode = 1#exploring mode entry

				elif self.hp_per_round <= 0:
					self.next_round()  

				elif self.current_mode == 1:
					if self.item_view == 1 and self.itemframe.count > 0:
						self.itemframe.use_item(self,self.focusing_object_id,None)

				elif self.current_mode == 2:
					print('Give up the puzzle, back to exploring mode')
					self.quit_puzzle_mode()

				elif self.current_mode == 3:
					if self.manual_node.type == 'tail': 
						self.remove_widget(self.prompt_label) 
						self.clear_text_on_screen()		
						self.complete_chapter = True


			#for testing
			elif press_key_id == 112:#p
				if self.current_mode == 1:	
					self.current_mode = 3
			elif press_key_id == 100:#d: 
				self.dialog_view ^= 1

			elif press_key_id == 115:#s
				if self.current_mode == 0 and not self.seal_on and not self.finish_auto:
					print('Skip the auto dialog')
					self.clear_text_on_screen()
					self.finish_auto = True
					#for testing
				if self.current_mode == 1: #DEBUG
					self.enter_puzzle_mode(64, 'synthesis')
			# elif press_key_id == 116:#t
			# 	if self.cur_unsafed:
			# 		self.testing_save_object_pos()
			# 	else:
			# 		self.testing_set_objects_pos()
			elif  press_key_id == 114:#r:
				if self.current_mode == 1:	
					if self.item_view == 1: 
						self.reload_item_list = True

			elif  press_key_id == 109:#m:
				if self.current_mode == 1:
					self.complete_chapter = True#DEBUG
			elif  press_key_id == 110:#n:
				if self.current_mode == 1:
					if self.item_view == 0: 
						self.next_round()

			elif press_key_id in [274,273]:
				# if self.cur_unsafed:
				# 	self.testing_modify_object_size(press_key_id)
				if self.current_mode == 1: 
					pass

			return True
	def key_release(self, *args):
		if self.manager.current == 'story':	
			#print('story key release: ',args)
			press_key_id = args[1]#args[1]:ASCII?

			return True	
	def map_objects_allocator(self, action):#TODO: 按照物件種類分類做，線索和普通物件無圖片，配置選取框範圍於地圖上即可
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
				for MapObject in self.objects_allocation[self.current_map_id]:#2D-list
					print('MapObject info:',MapObject.object_id ,MapObject.map_name)
					self.mapobjects_register.append(MapObject)
					self.add_widget(MapObject)


	def exploring_maps(self, press_key_id):

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

	def generate_item_tag(self):
		print("Enter function: generate_item_tag")
		#RGB (0,182,237)
		self.item_tag = Image(pos_hint={'x':.97,'y':.77},size_hint=(.03,.08),source='res/images/itemtag.png',allow_stretch=True,keep_ratio=False)#ImageButton(pos_hint={'x':.97,'y':.77},size_hint=(.03,.08),source='res/images/itemtag.png',callback=self.display_itemframe,allow_stretch=True,keep_ratio=False)
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
					print('add item source:',item.source)
					if item not in self.children:
						self.add_widget(item)		
					else:
						print(f'[*]Exception: item:{item} is already in the screen')
				if self.itemframe.count > 0:
					self.itemframe.focusing_frame_id = self.itemframe.cyclic[0]#->auto_focus->auto_focus_item->dragging generate
				else:
					self.itemframe.focusing_frame_id = -1
				#make sure the dragging is inside box canvas

			self.canvas_on_item_images()
		
			#select button

		elif action == 'hide':
			
			self.canvas.remove_group('cap')
			self.itemframe.focusing_frame_id = -1 #-> focusing_object_id = -1 (remove_widget of itemframe.item_images)
			self.canvas.remove_group('itemicon') 

	def canvas_under_item_images(self):#TODO:道具欄按鍵提示(->,<-,Enter,i,click,...)
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
		for i in table.keys():
			print(f'table[{i}][\'line\']:',table[i]['line'])
			print('self.manual_node.text_line:',self.manual_node.text_line)
			if len(table[i]['line'].split(':')) > 1:
				table_line =  table[i]['line'].split(':')[1]
			else:
				table_line = table[i]['line']
			if table_line == self.manual_node.text_line.strip('\n'):
				print('Switch bg to:',table[i]['source'])
				bg = Rectangle(source=table[i]['source'], pos=(0,0), size=(self.w,self.h),group='bg')
				self.bg_widget.load_bg(bg)
				break

		if self.manual_node.type != 'tail':
			self.clear_text_on_screen()
			node = self.manual_node = self.manual_node.get_next()
			print('self.manual_node.text_line:',self.manual_node.text_line)
			self.lastline_time = line_display_scheduler(self,node.text_line,False,special_char_time,next_line_time,common_char_time,name=node.speaker)
		else:
			#prompt to next chapter, end round
			auto_prompt(self,'Enter',{'x':.25,'y':.4},instance=self, prompt=True,extra_info='Complete chapter!\n')

	def last_dialog(self,*args):		
		if self.manual_node.type != 'head':
			self.clear_text_on_screen()
			node = self.manual_node = self.manual_node.get_last()
			self.lastline_time = line_display_scheduler(self,node.text_line,False,special_char_time,next_line_time,common_char_time,name=node.speaker)

	#TODO: 計時器功能
	def enter_puzzle_mode(self, object_id, behavior_type):#TODO: 原本在地圖上的會有自己的判定範圍
		self.probing = False
		self.current_mode = 2#open item view
		self.canvas.add(Color(rgba=(.2,.2,.2,.2),group='puzzle_mode'))
		self.canvas.add(Rectangle(pos=self.pos,size=self.size,group='puzzle_mode'))
		item = GM.object_table[str(object_id)]
		print('puzzle_mode item:',item)
		self.behavior_type = behavior_type
		if behavior_type == 'puzzle':
			self.puzzle_handler(item)
		elif behavior_type == 'lock': 
			self.lock_handler(item)
		elif behavior_type == 'synthesis': 
			self.synthesis_handler(item)
		
	def puzzle_handler(self, item):#TODO: 目前只有密碼鎖一種
		self.puzzle_name = item['name']
		if self.puzzle_name == '木製保險櫃(關)':
			self.puzzling = True
			build_CodedLock(self,item)#TODO:item source

		else:
			print('目前不支援')

	def synthesis_handler(self, item):#TODO: canvas 框(填入已知)+框(待填)=框 拖曳正確輸入就產生輸出道具
		material = item['name']  
		synthesis_content = GM.synthesis_table[material]
		expected_input = synthesis_content['input']
		if self.item_view == 0:
			self.item_view = 1
		synthesis_canvas(self,item,0)
		if self.itemframe.count > 0:
			self.global_mouse_event = Clock.schedule_interval(global_mouse, 0.1)
			self.synthesis_event = Clock.schedule_interval(partial(self.material_item_judge,item,synthesis_content), 0.1)

	def material_item_judge(self,item,synthesis_content,*args):

		def try_synthesis(screen,expected_input,dragging_object_id,*args):
			if GM.object_table[str(dragging_object_id)]['name'] == expected_input:
				print('取消前 screen.synthesis_event:',screen.synthesis_event)
				screen.synthesis_event.cancel()
				print('取消後 screen.synthesis_event:',screen.synthesis_event)
				screen.global_mouse_event.cancel()
				GM.players[screen.current_player_id].spend_item(dragging_object_id)
				print('合成成功...獲得新道具!')
				screen.quit_puzzle_mode(text='合成成功...獲得新道具!')
				#WARNING: name_to_id可能重複
				output_id = GM.name_to_id_table[synthesis_content['output']]
				synthesis_canvas(self,item,2,GM.object_table[str(output_id)]['source'])
				GM.players[screen.current_player_id].get_item(output_id)

			else:
				print('合成失敗!')#DEBUG
				screen.clear_text_on_screen()
				spent_time = line_display_scheduler(screen,'合成失敗...',False,special_char_time,next_line_time,common_char_time)
				#Clock.schedule_once(screen.clear_text_on_screen,spent_time+.5)
				#screen.clear_text_on_screen(delay_time=spent_time+.5)
				Clock.schedule_once(partial(screen.dragging.reset,screen,2),spent_time+.5) 		
				self.canvas.remove_group('synthesis1')
			#screen.hp_per_round -= 1#DEBUG: 連續扣血問題

		expected_input = synthesis_content['input']
		dragging_object_id = self.itemframe.item_list[self.itemframe.cyclic[0]] 
		if E2_distance(self.dragging.stopped_pos,(global_x,global_y))< 10 and self.mouse_in_range({'x':.34,'y':.6} ,(.12,.2)):
			print('嘗試合成')
			self.remove_widget(self.dragging)
			#synthesis_canvas(self,item,1,self.dragging.source)
			Clock.schedule_once(partial(synthesis_canvas,self,item,1,self.dragging.source),.1)
			#Clock.schedule_once(partial(synthesis_canvas,self,item,stage=2),1)
			Clock.schedule_once(partial(try_synthesis,self,expected_input,dragging_object_id),1)
		elif not self.mouse_in_range({'x':.34,'y':.6} ,(.12,.2)) and self.dragging.free == 1 :

			print('合成超出範圍，返回原位')		
			self.dragging.reset(self,2)

	def lock_handler(self, item):#原image消失?背景模糊?對話框顯示物件敘述
		lock_name = item['name']
		lock_content = GM.unlock_table[lock_name]
		expected_input = lock_content['input_item']
		# self.lock = Image(source=item['source'],pos_hint ={'x':.4,'y':.4},size_hint=(.2,.2) ,allow_stretch=True,keep_ratio=False)
		# self.add_widget(self.lock)
		if self.item_view == 0:
			self.item_view = 1

		judge_pos_hint, judge_size_hint = {'x':.35,'y':.35},(.3,.3)
		if item['source'] is not None:
			self.canvas.add(Rectangle(source=item['source'],pos=(.35*global_w,.35*global_h),size=(.3*global_w,.3*global_h),group='lock'))
		else:
			judge_pos_hint, judge_size_hint = item['pos_hint'], item['size_hint']
		if self.itemframe.count > 0:
			self.global_mouse_event = Clock.schedule_interval(global_mouse, 0.1)
			self.lock_event = Clock.schedule_interval(partial(self.key_item_judge,lock_content,judge_pos_hint, judge_size_hint), 0.1)

	def key_item_judge(self, lock_content, judge_pos_hint, judge_size_hint, *args):
		expected_input = lock_content['input_item']
		dragging_object_id = self.itemframe.item_list[self.itemframe.cyclic[0]] 
		if E2_distance(self.dragging.stopped_pos,(global_x,global_y))< 10 and self.mouse_in_range({'x':.4,'y':.4},(.2,.2)):
			print('GM.object_table[str(dragging_object_id)][\'name\']:',GM.object_table[str(dragging_object_id)]['name'] )
			print('expected_input:',expected_input)
			if GM.object_table[str(dragging_object_id)]['name'] == expected_input:#開鎖成功
				self.lock_event.cancel()
				self.global_mouse_event.cancel()
				GM.players[self.current_player_id].spend_item(dragging_object_id)#->auto_reload_item_list->auto_gen_items	



				#lock_output: output item, new scene, trigger
				if lock_content['output_item'] is not None:
					print('開鎖成功...獲得新道具!')
					self.quit_puzzle_mode(text='開鎖成功...獲得新道具!')
					#WARNING: name_to_id可能重複
					output_id = GM.name_to_id_table[lock_content['output_item']]
					GM.players[self.current_player_id].get_item(output_id)#->auto_reload_item_list->auto_gen_items	
				if lock_content['new_scene'] is not None:
					print('開鎖成功...解鎖新場景!')
					self.quit_puzzle_mode(text='開鎖成功...解鎖新場景!')

					name = lock_content['new_scene'].split('\'')[1]
					GM.Chapters[self.current_player_id][self.current_chapter].unlock_new_map(name)
					self.current_map_id = len(self.chapter_maps) - 1 #unlock and go to new scene
				if lock_content['trigger']:
					print('開鎖成功...觸發劇情!')	
					self.quit_puzzle_mode(text='開鎖成功...觸發劇情!',turn_mode=3)

			else:
				print('開鎖失敗!')#DEBUG:沒顯示
				self.clear_text_on_screen()
				spent_time = line_display_scheduler(self,'開鎖失敗...',False,special_char_time,next_line_time,common_char_time)
				#Clock.schedule_once(self.clear_text_on_screen,spent_time+.3)
				#self.clear_text_on_screen(delay_time=spent_time+.3)	
				self.dragging.reset(self,2)

			#self.hp_per_round -= 1
		elif not self.mouse_in_range(judge_pos_hint, judge_size_hint) and self.dragging.free == 1:#DEBUG: 會扣血
			print('開鎖超出範圍，返回原位')		
			self.dragging.reset(self,2)

	def mouse_in_range(self,pos_hint,size_hint):
		#print('global_x,global_y:',global_x,global_y)	
		xh = global_x/global_w
		yh = global_y/global_h
		if xh >= pos_hint['x'] and xh <= pos_hint['x']+size_hint[0] and \
		yh >= pos_hint['y']	and yh <= pos_hint['y']+size_hint[1]:
			return True
		else:
			return False

	def quit_puzzle_mode(self,text='再試試看吧...',turn_mode=1):

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
			#self.remove_widget(self.lock)	
			self.canvas.remove_group('lock')	
		elif self.behavior_type == 'synthesis':
			print('quit synthesis')
			try:
				self.synthesis_event.cancel()
				self.global_mouse_event.cancel()		
			except:
				pass
			self.canvas.remove_group('synthesis')
			self.canvas.remove_group('synthesis1')
		self.clear_text_on_screen()
		spent_time = line_display_scheduler(self,text,False,special_char_time,next_line_time,common_char_time)
		#Clock.schedule_once(self.clear_text_on_screen,spent_time+.5)
		#self.clear_text_on_screen(delay_time=spent_time+.5)
		self.remove_widget(self.dragging)

		self.current_mode = turn_mode
		if self.item_view == 1:
			Clock.schedule_once(self.try_close_item_view,spent_time+.5)
		else:
			self.try_close_dialog_view()
			# if self.dialog_view == 1:
			# 	self.dialog_view = 0

	#TODO: implement object functions here, btn must be an instance of MapObject
	def on_press_item(self, btn):
		self.hp_per_round -= 1
		object_id = btn.object_id
		self.pickup_chapter_objects(object_id,btn)

		self.dialog_view = 1
		spent_time = line_display_scheduler(self,'好像撿到有用的道具了呦',False,special_char_time,next_line_time,common_char_time)
		self.delay_hide_dialogframe(spent_time)

	def pickup_chapter_objects(self, object_id,btn,action='to_bag'):
		picked_item = None
		for MapObject in self.objects_allocation[self.current_map_id]:
			if MapObject.object_id == object_id:
				picked_item = MapObject
				print('picked_item:',picked_item.object_id)
				break

		GM.Chapters[self.current_player_id][self.current_chapter].chapter_objects[self.current_map_id].remove(picked_item)#
		#self.objects_allocation[self.current_map_id].remove(picked_item)
		if action == 'to_bag':
			GM.players[self.current_player_id].get_item(object_id)
		self.remove_widget(btn) 


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

		#獲得敘述中道具
		item_name = text_line[text_line.find('（')+1:text_line.find('）')].split('：')[1]
		print('獲得敘述中道具:',btn,item_name)
		item_id = GM.name_to_id_table[item_name]
		GM.players[self.current_player_id].get_item(item_id)
		self.pickup_chapter_objects(btn.object_id,btn,action='discard')	

		#map_objects_a
	def on_press_switching(self,btn):
		self.probing = False
		new_scene_name = btn.object_content['name']
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
			text_line = '不太清楚這有什麼用...'
		spent_time = line_display_scheduler(self,text_line,False,special_char_time,next_line_time,common_char_time)
		self.delay_hide_dialogframe(spent_time)

	def delay_hide_dialogframe(self, delay_time):#TODO: 這裡可能會有殘留，改成對話前清空
		print('delay hide dialogframe')
		print('self.displaying_character_labels:',self.displaying_character_labels)
		Clock.schedule_once(self.try_close_dialog_view,delay_time+.1)
		#Clock.schedule_once(self.clear_text_on_screen,delay_time)
		self.clear_text_on_screen(delay_time=delay_time)
		def probing_free(screen,*args):
			self.probing = False
		Clock.schedule_once(partial(probing_free,self),delay_time+.2)

	def try_close_dialog_view(self,*args):
		if self.dialog_view == 1:
			self.dialog_view = 0	

	def try_close_item_view(self,*args):
		if self.item_view == 1:
			self.item_view = 0

	def clear_text_on_screen(self,uncontinuous=True,delay_time=0,*args):#TODO:clear_text_on_screen如何與line_display_scheduler對應之同步問題
		print('[*]clear_text_on_screen!!')
		def cancel_events(screen,*args):
			for event in screen.dialog_events:
				event.cancel()	
		#delay at here
		if delay_time > 0:
			Clock.schedule_once(partial(cancel_events,self), delay_time) 
			Clock.schedule_once(partial(clear_displayed_text,self,self.displaying_character_labels), delay_time)
		else:
			cancel_events(self)
			clear_displayed_text(self,self.displaying_character_labels)
		
		if uncontinuous:
			self.dialog_events = []	

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
	# 	#TODO:對於每個物件表的'clue','nothing'產生選取框把判定範圍標示出來，並存到allocate_all_objects_table.json裡面

	# 	pass


	#for testing: 
	def testing_golden_finger(self):#直接通過章節或直接完成遊戲的通關密碼
		pass


	#TODO
	def load_game(self):
		GM.load_game(self)

	def auto_save_game(self,*args):
		if not self.loading:
			GM.save_game(self)		
			#TODO: 按照修改的資料種類傳參數進去改寫部分紀錄檔即可


	@staticmethod
	def exit_game():
		exit()


def global_mouse(*args):
	global global_x,global_y
	#global_h = get_screen_size()[1]
	if OS == "Darwin": #Macbook
		global_x, global_y = pygame.mouse.get_pos()#Bugs in Windows
		global_y = global_h - global_y
	elif OS == "Windows":#Windows
		_,_,(global_x, global_y) = win32gui.GetCursorInfo()
		global_y = global_h - global_y