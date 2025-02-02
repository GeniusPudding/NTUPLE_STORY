# -*- coding: utf-8 -*-
###################################################
# Manage all of the game status here              #
# "Screen" must be an intance og kivy Screen      #
###################################################
from globals import *
from subgames import *
from dialog_utils import *
from UI_utils import *

player_name = {0:'李詠晴',1:'楊承恩',2:'孟亦廷',3:'張怡彤'}
turns = {1:2,2:3,3:0,0:1}
class GameManagerScreen(Screen):#main control class of the whole game
	#TODO: 用計時器跟體力控制做出不同難度模式，預設為easy，不限時
	p0 = ObjectProperty()
	p1 = ObjectProperty()
	p2 = ObjectProperty()
	p3 = ObjectProperty()
	players = ReferenceListProperty(p0,p1,p2,p3)
	def __init__(self, **kwargs):
		super(GameManagerScreen, self).__init__(**kwargs)
		#init all needed game info here
		self.p0 = Player(0,self)
		self.p1 = Player(1,self) 
		self.p2 = Player(2,self) 
		self.p3 = Player(3,self)
		self.current_player_id = 3
		self.current_chapter = [0]*4
		self.players_name = {0:'室友',1:'男友',2:'哥哥',3:'故人'}
		self.object_table = self.load_object_table()
		self.unlock_table = self.load_unlock_table()
		self.synthesis_table = self.load_synthesis_table()
		self.puzzle_table = self.load_puzzle_table()
		self.name_to_id_table = self.load_name_to_id_table() 

	def link_main_screen(self):
		self.main_screen = self.manager.get_screen('story')
		self.Chapters = self.init_chapters(self.main_screen)
		self.main_screen.start_story(self)		

	def start_chapter(self):
		self.Chapters[self.current_player_id][self.current_chapter[self.current_player_id]].started = True

	def change_turn(self):
		print('turns:',turns)
		print('self.current_chapter:',self.current_chapter)
		if len(turns) == 0:
			self.ready_to_ending()
			return self.current_player_id, self.current_chapter[self.current_player_id]
		
		self.current_player_id = turns[self.current_player_id]
		return self.current_player_id, self.current_chapter[self.current_player_id]

	def change_chapter(self):
		if self.current_chapter[self.current_player_id] == final_chapter:
			self.exclude_from_turns(self.current_player_id)#set current_player_id to last player, for the change_turn

		else:
			#testing
			self.players[self.current_player_id].unread_achievement\
				.append(self.current_chapter[self.current_player_id])


			self.current_chapter[self.current_player_id] += 1

	def exclude_from_turns(self, player_id):
		global turns
		new_link = {}
		new_key = 0
		new_val = 0
		for key, val in turns.items():
			if val == player_id and key == player_id:
				turns = {} 
				return
			if val == player_id or key == player_id:
				if val == player_id:
					self.current_player_id = new_key = key

				else:
					new_val = val
				
			else:
				new_link[key] = val
		new_link[new_key] = new_val


		turns = new_link

	def ready_to_ending(self):
		self.manager.get_screen('ending').load_ending()
		self.manager.current = 'ending'

	def init_chapters(self,main_screen):
		Chapters = []
		for p in range(4):
			Chapters.append([])
			for r in range(4):
				Chapters[p].append(Chapter(player_id=p, chapter_id=r,main_screen=main_screen))
		return Chapters
	def load_object_table(self):
		#'id':{'name','source','pos_hint','size_hint','player','chapter','function_types','description','on_map_name'}
		with open('res/objects/final_objects_table.json','r') as f:
			table = json.load(f)
		return table

	def	load_unlock_table(self):
		with open('res/objects/unlock_table.json','r',encoding='utf-16') as f:
			table = json.load(f)
		return table 

	def load_synthesis_table(self):
		with open('res/objects/synthesis_table.json','r') as f:
			table = json.load(f)
		return table 	

	def load_puzzle_table(self):
		with open('res/objects/puzzle_table.json','r') as f:
			table = json.load(f)
		return table 	

	def load_name_to_id_table(self):
		with open('res/objects/name_to_id_table.json','r') as f:
			table = json.load(f)
		return table 	

	def load_game(self,main_screen):
		pickle_list = ['0_0.pickle','0_1.pickle','0_2.pickle','0_3.pickle',\
		'1_0.pickle','1_1.pickle','1_2.pickle','1_3.pickle',\
		'2_0.pickle','2_1.pickle','2_2.pickle','2_3.pickle',\
		'3_0.pickle','3_1.pickle','3_2.pickle','3_3.pickle',\
		'p0.pickle','p1.pickle','p2.pickle','p3.pickle','current_c_p.pickle','main_screen.pickle']
		pickle_path = 'res/pickles/'
		
		if set(pickle_list) - set(os.listdir(pickle_path)) != set():#缺少記錄檔
			for f in os.listdir(pickle_path):
				if '.pickle' in f:
					os.remove(os.path.join(pickle_path,f))#reset
			main_screen.next_round()
			return

		print('[*]Loading game records...')	 
		for p in range(4):
			player = f'p{p}.pickle'
			p_ = open(os.path.join(pickle_path,player), 'rb')
			p_dict = pickle.load(p_)
			self.players[p].item_list = p_dict['item_list']#DEBUG: 地圖上還有重複載入
			self.players[p].unread_achievement = p_dict['unread_achievement']
			print(f'Load {p}\'s p_dict:{p_dict}')
			for c in range(4):
				chapter = f'{p}_{c}.pickle' 
				c_ = open(os.path.join(pickle_path,chapter), 'rb')
				c_dict = pickle.load(c_) 
				print(f'Load {p}_{c}\'s c_dict:{c_dict}')
				self.Chapters[p][c].chapter_maps = c_dict['chapter_maps']
				self.Chapters[p][c].new_map_reallocation()
				self.Chapters[p][c].started = c_dict['started']
				self.Chapters[p][c].picked_item_info = c_dict['picked_ids'] 
				for (m_id,i_id) in self.Chapters[p][c].picked_item_info:#TODO:改善效率
					print('m_id,i_id:',m_id,i_id)
					for mapobject in self.Chapters[p][c].chapter_objects_of_maps[m_id]:
						if mapobject.object_id == i_id:
							self.Chapters[p][c].chapter_objects_of_maps[m_id].remove(mapobject)
				print('load self.Chapters[p][c].chapter_objects_of_maps:',self.Chapters[p][c].chapter_objects_of_maps)
				#TODO:load picked item ids and remove from chapter map objects
		p_c = open(os.path.join(pickle_path,'current_c_p.pickle'), 'rb')	
		dict_p_c = pickle.load(p_c) 	
		print(f'Load dict_p_c:{dict_p_c}')
		self.current_player_id = dict_p_c['current_player_id']
		self.current_chapter = dict_p_c['current_chapter'] 

		#main_screen.loading = True
		main_screen.current_player_id, main_screen.current_chapter = self.current_player_id, self.current_chapter[self.current_player_id]	
		main_screen.auto_reload_chapter_info(self,[main_screen.current_player_id, main_screen.current_chapter])
		main_screen.current_player = player_name[main_screen.current_player_id]

		main = open(os.path.join(pickle_path,'main_screen.pickle'), 'rb')	
		dict_main = pickle.load(main)	
		print(f'Load dict_main:{dict_main}')
		load_mode = dict_main['current_mode'] 
		if load_mode == 0:
			main_screen.current_mode = -1
		main_screen.current_mode = load_mode
		global turns
		turns = dict_main['turns']
		print('load turns:',turns)
		#main_screen.hp_per_round = 20#dict_main['hp_per_round']
		#main_screen.current_map_id = -1
		main_screen.current_map_id = dict_main['current_map_id']
		#main_screen.reload_item_list = True
		if load_mode == 3:#mode3載入時會先被關對話框
			Clock.schedule_once(main_screen.try_open_dialog_view,1) 
		main_screen.loading = False

	def save_game(self,main_screen):#map_objects_allocator 
		pickle_path = 'res/pickles/'
		for p in range(4):
			player = f'p{p}.pickle'
			p_ = open(os.path.join(pickle_path,player), 'wb')
			p_dict = {'item_list':self.players[p].item_list,'unread_achievement':\
			self.players[p].unread_achievement}
			pickle.dump(p_dict,p_) 
			print('auto save p_dict:',p_dict)
			for c in range(4):		
				chapter = f'{p}_{c}.pickle' 
				c_ = open(os.path.join(pickle_path,chapter), 'wb')
				c_dict = {'chapter_maps':self.Chapters[p][c].chapter_maps,\
				'started':self.Chapters[p][c].started,'picked_ids':self.Chapters[p][c].picked_item_info}		
				print('auto save c_dict:',c_dict)
				pickle.dump(c_dict,c_) 
		p_c = open(os.path.join(pickle_path,'current_c_p.pickle'), 'wb')	
		dict_p_c = {}
		dict_p_c['current_player_id'] = self.current_player_id 
		dict_p_c['current_chapter'] = self.current_chapter				
		pickle.dump(dict_p_c,p_c) 
		print('auto save dict_p_c:',dict_p_c)
		main = open(os.path.join(pickle_path,'main_screen.pickle'), 'wb')	
		dict_main = {}	
		dict_main['current_mode'] = main_screen.current_mode
		if main_screen.current_mode == 2:
			dict_main['current_mode'] = 1
		# dict_main['hp_per_round'] = main_screen.hp_per_round	
		dict_main['turns'] = turns
		dict_main['current_map_id'] = main_screen.current_map_id
		print('auto save dict_main:',dict_main)
		pickle.dump(dict_main,main) 

class Player(object):
	def __init__(self, player_id, GM):
		self.GM = GM
		self.name = ''
		self.personality = ''
		self.item_list= []#only int key
		self.unread_achievement = []
	def get_item(self, object_id):#No need to consider number of item
		if object_id not in self.item_list:
			print('get_item:',object_id)
			self.item_list.append(object_id)#key:object_id,value:(name,source,location,pos,player,chapter,function_types,description)
			self.GM.manager.get_screen('story').reload_item_list = True 
		else:
			print('[*] Exception! Cannot get an item again!')
	def spend_item(self, object_id):
		if object_id in self.item_list:
			print('spend_item:',object_id)
			self.item_list.remove(object_id)#key:object_id,value:(name,source,location,pos,player,chapter,function_types,description)
			self.GM.manager.get_screen('story').reload_item_list = True 
		else:
			print('[*] Exception! Cannot spend an item that not in item list!')

class Chapter(object):
	def __init__(self, player_id, chapter_id,main_screen):
		self.object_path = f'res/chapters/{player_id}_{chapter_id}/objects/' #including a json and object images
		self.map_path = f'res/chapters/{player_id}_{chapter_id}/maps/'  #including map images
		self.unlocked_map_path = f'res/chapters/{player_id}_{chapter_id}/unlocked_maps/'  #including unlocked map images
		self.dialog_path = f'res/chapters/{player_id}_{chapter_id}/dialogs/' #including two txt files
		self.scene_path = f'res/chapters/{player_id}_{chapter_id}/scenes/' #including scene images for the plot mode
		self.npc_path = f'res/chapters/{player_id}_{chapter_id}/NPCs/' #including json of NPC info
		self.player_chapter = (player_id,chapter_id)
		self.main_screen = main_screen
		self.chapter_maps = self.load_chapter_maps()
		self.chapter_default_map = self.load_chapter_default_map(player_id, chapter_id)
		self.chapter_NPCs_of_maps = self.load_chapter_NPCs_of_maps()#list of ImageButton
		self.chapter_objects_of_maps = self.load_chapter_objects_of_maps() #objects_allocation[current_map] = list of MapObjects 
		self.picked_item_info = []#TODO: save/load the picked item ids
		self.chapter_plot_scenes = self.load_plot_scenes()
		self.chapter_scenes_table = self.load_scenes_table()
		self.chapter_title = self.load_chapter_title(player_id, chapter_id)
		self.chapter_pre_plot, self.chapter_plot = self.load_chapter_dialogs()#self.chapter_predialog,self.chapter_postdialog
		self.started = False

	def remove_objects_on_map(self,map_id,picked_item):
		print('self.chapter_objects_of_maps[map_id]:',self.chapter_objects_of_maps[map_id])
		print('picked_item:',picked_item)
		self.chapter_objects_of_maps[map_id].remove(picked_item)
		self.picked_item_info.append((map_id,picked_item.object_id))
		self.main_screen.remove_widget(picked_item)

	def unlock_new_map(self,map_name):#TODO: Optimize,不需要重新載入所有地圖物件
		for locked_img in os.listdir('res/images/handpainting'):#self.locked_map_path
			if map_name == locked_img.split('.')[0]:
				shutil.copy(os.path.join('res/images/handpainting/',locked_img),self.unlocked_map_path)
				self.chapter_maps.append(os.path.join(self.unlocked_map_path,locked_img))
				break
		self.new_map_reallocation()

	def new_map_reallocation(self):	
		self.main_screen.chapter_maps = self.chapter_maps#reload main screen's info
		self.main_screen.objects_allocation = self.chapter_objects_of_maps\
		 = self.load_chapter_objects_of_maps()#load new objects info of unlocked map
		self.main_screen.NPCs_allocation = self.chapter_NPCs_of_maps\
		 = self.load_chapter_NPCs_of_maps()#load new objects info of unlocked map
	


	def load_chapter_default_map(self,player_id, chapter_id):

		default_maps = ['雙人宿舍夜','博雅','雙人宿舍日','雙人宿舍日','農場夜',\
		'B男宿舍夜','排球場','女主家裡房間一','女主家C男房間晚一','女主家C男房間晚一','女主家客廳',\
		'女主家C男房間晚二','D女房間','D女房間','D女房間二','D女房間二']
		for i,m in enumerate(self.chapter_maps):
			if default_maps[player_id*4+chapter_id] in m:
				return i
		return 0

	def load_chapter_dialogs(self):

		f1 = open(os.path.join(self.dialog_path,'1.txt'),'r',encoding='utf-16')		
		pre =[line for line in f1.read().split('\n') if len(line)>0]
		part1 = []
		for line in pre:
			line_list = line.split(':')
			if len(line_list)>1:
				part1.append([line_list[0],line_list[1]])
			else:
				part1.append(['',line])

		f2 = open(os.path.join(self.dialog_path,'2.txt'),'r',encoding='utf-16')
		post = [line for line in f2.read().split('\n') if len(line)>0]
		part2 = []
		for line in post:
			line_list = line.split(':')
			if len(line_list)>1:
				part2.append([line_list[0],line_list[1]])
			else:
				part2.append(['',line])
		return part1,part2

	def load_chapter_title(self,player_id, chapter_id):

		text = ['紊亂的書房','曾經的約定','蜷曲的背影','生日的禮物','蒼白的生日','錯位的戀情','青鳥的囚籠','友誼的裂痕','超載的負荷','哭泣的日記','哭泣的玩偶','遺失的過往','手機的密碼','補全的卡片','渴望的支持','友誼的結尾'][4*chapter_id+player_id]
		return Label(text=text,color=(191/255, 201/255, 202/255, 1),pos_hint={'x':.25,'y':.4},size_hint=(.5,.3),halign='center',valign='center',font_size=184,font_name='res/mona.otf')#  'res/HuaKangTiFan-CuTi-1.otf')
	def load_chapter_objects_of_maps(self):

		maps = self.chapter_maps
		print('load chapter maps:',maps)
		chapter_objects = []
		for i in range(len(maps)):
			chapter_objects.append([])

		with open(self.object_path+'chapter_objects.json','r',encoding='utf-16') as f:
			objects_table = json.load(f)
			for str_id in  objects_table.keys():
				obj = objects_table[str_id]
				if obj['on_map_name'] is not None:
					if obj['pos_hint'] is not None and obj['size_hint'] is not None:
						on_map = 0
						for map_id,map_path in enumerate(maps):
							if obj['on_map_name'] == map_path.split('/')[-1].split('.')[0]:
								objname = obj['name']
								print(f'map id:{map_id}, name:{objname}  allocate object id:{str_id}')
								chapter_objects[map_id].append(MapObject(screen=self.main_screen, object_id=int(str_id),object_content=obj,\
								size_hint=obj['size_hint'],pos_hint={'x':obj['pos_hint'][0],'y':obj['pos_hint'][1]}))
								on_map = 1
								break
						if not on_map:#DEBUG
							name = obj['on_map_name'] 
							print(f'[*] Exception! Can\'t find object:{obj}, object[\'on_map_name\']:{name}\'s map!')
							#可能是需要解鎖的場景圖
					else:
						print(f'[*] Exception! object:{obj} 資料不足') 

		# MapObject
		print('chapter_objects:',chapter_objects)
		return chapter_objects
	
	def load_chapter_NPCs_of_maps(self):
		maps = self.chapter_maps
		print('load chapter maps:',maps)
		npc_buttons = []
		for i in range(len(maps)):
			npc_buttons.append([])
		if not os.path.isfile(os.path.join(self.npc_path,'npc_info.json')):
			return npc_buttons
		count = 0
		with open(os.path.join(self.npc_path,'npc_info.json'),'r') as f:
			table = json.load(f)
			for map_id,map_path in enumerate(self.chapter_maps):
				for i in table.keys():
					if table[i]['map_name'] == map_path.split('/')[-1].split('.')[0]:#
						npc_buttons[map_id].append(NPCButton(self.main_screen,table[i]['dialog'],self.player_chapter[0],table[i]['get_item'],'res/images/choices.png',\
							pos_hint={'x':.375,'y':.3+.2*count},size_hint=(.25,.1),background_color=(1,1,1,0), color=(0,0,0,1),text=table[i]['npc_name'],font_size=40,font_name= 'res/HuaKangTiFan-CuTi-1.otf' ))
						count += 1
				count = 0

		print('create npc_buttons:',npc_buttons)
		return npc_buttons		

	def load_plot_scenes(self):
		s = []
		for img in os.listdir(self.scene_path):
			if '.png' in img or '.jpg' in img:
				s.append(img)
		return s

	def load_scenes_table(self):
		with open(os.path.join(self.scene_path,'plot_scenes.json'),'r') as f:
			table = json.load(f)
		return table

	def load_chapter_maps(self):

		chapter_maps = []
		for f in os.listdir(self.map_path):
			if '.jpg' in f or '.png' in f:
				chapter_maps.append(os.path.join(self.map_path,f))
		print('chapter_maps:',chapter_maps)
		return chapter_maps

class NPCButton(Button):#text = npc_name
	def __init__(self,main_screen,dialog,player_id,get_item,source,**kargs):
		super(NPCButton, self).__init__(**kargs)
		self.main_screen = main_screen
		self.dialog = dialog
		self.get_item = get_item
		self.player_id = player_id
		self.bind(parent=self.on_add_and_remove)
		self.source = source
	def delay_release_NPC(self,*args):
		self.main_screen.NPC_talking = False
	def on_press(self):	
		if not self.main_screen.NPC_talking:
			self.main_screen.NPC_talking = True
			for l in self.main_screen.displaying_character_labels:
				print('l.text:',l.text)
			self.main_screen.clear_text_on_screen()
			spent_time = line_display_scheduler(self.main_screen,self.dialog,False,special_char_time,next_line_time,common_char_time,uncontinuous=True)
			self.main_screen.clear_text_on_screen(delay_time=spent_time)
			for l in self.main_screen.displaying_character_labels:
				print('after l.text:',l.text)
			if self.get_item  is not None:
				self.main_screen.get_item_from_NPC(self.get_item)
			#self.main_screen.hp_per_round -= 1
			Clock.schedule_once(self.delay_release_NPC,spent_time)
			Clock.schedule_once(self.main_screen.try_close_dialog_view,spent_time)

	def on_add_and_remove(self,isinstance,parent):
		if parent is not None:
			print(f'Add NPCButton:{self.text} on main screen!')
			self.main_screen.canvas.add(Color(rbga=(1,1,1,1),group='npc'))
			self.main_screen.canvas.add(Rectangle(source='res/images/choices.png',pos=(self.pos_hint['x']*global_w,self.pos_hint['y']*global_h),\
				size=(self.size_hint[0]*global_w,self.size_hint[1]*global_h),group='npc'))
		else:
			print(f'Remove NPCButton:{self.text} on main screen!')	 
			self.main_screen.canvas.remove_group('npc')

class MapObject(Widget):#自定義按紐
	def __init__(self,object_id,object_content,screen,touch_range='default', **kargs):
		#依照是否有source圖片區分
		super(MapObject, self).__init__(**kargs)
		self.object_id = object_id
		self.source = object_content['source']
		self.object_content = object_content
		self.object_types = object_content['function_types']
		self.map_name = object_content['on_map_name']
		self.screen = screen
		self.used = False
		if self.source is None:
			self.canvas.add(Color(rgba=(1,1,1,0),group='mapobject'))
			self.canvas.add(Rectangle(pos=(self.pos_hint['x']*global_w,self.pos_hint['y']*global_h),\
				size=(self.size_hint[0]*global_w,self.size_hint[1]*global_h),group='mapobject'))
		else:
			self.canvas.add(Color(rgba=(1,1,1,1),group='mapobject'))
			self.canvas.add(Rectangle(source=self.source,pos=(self.pos_hint['x']*global_w,self.pos_hint['y']*global_h),\
				size=(self.size_hint[0]*global_w,self.size_hint[1]*global_h),group='mapobject'))

		if touch_range == 'default':
			self.touch_range = self.size_hint
		else:
			self.touch_range = touch_range

	def on_touch_down(self,touch):
		
		if self.collide_point(*touch.pos) and self.screen.current_mode == 1:
			print(f"Map object on_touch_down touch.pos:{touch.pos}")
			self.probe_object_on_map()

	def probe_object_on_map(self,*args):
		print(f'self:{self},args:{args}')
		screen = self.screen#args[1]
		print(f'probe self.object_id:{self.object_id},self.object_types:{self.object_types}')
		if isinstance(self,MapObject) and screen.current_mode == 1 and screen.item_view == 0 and not screen.probing:
			screen.probing = True
			if 'item' in self.object_types:
				#定義: 可以收進"道具欄"
				screen.on_press_item(self)
			else:
				if 'puzzle' in self.object_types:
					#定義: 物件需要輸入正確密碼，以打開該物件；例如[密碼鎖]
					screen.on_press_puzzle(self) 
				if 'lock' in self.object_types:
					#定義: 將正確道具拖曳至此物件，以打開該物件；例如[鑰匙]
					screen.on_press_lock(self) 
				if 'synthesis' in self.object_types:
					#定義: 可以跟另一樣道具合成產生新道具
					screen.on_press_synthesis(self)
				if 'clue' in self.object_types:
					#定義: 作為遊戲所需要的關鍵資訊
					screen.on_press_clue(self) 
				if 'trigger' in self.object_types:
					#定義: 點擊即觸發進入劇情模式
					screen.on_press_trigger(self) 
				if 'switching' in self.object_types:
					#定義: 點擊切換場景用
					screen.on_press_switching(self) 	
				if 'nothing' in self.object_types:
					#定義: 無特別功用
					screen.on_press_nothing(self) 				
				
# >>> def keep(path):
# ...     dir = os.listdir(path)
# ...     if len(dir) == 0:
# ...             f = open(os.path.join(path,'.keep'),'w')
# ...             f.close()
# ...     for d in dir:
# ...             if os.path.isdir(os.path.join(path,d)):
# ...                     keep(os.path.join(path,d))
# ...
# >>> keep('./')