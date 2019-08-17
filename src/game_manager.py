# -*- coding: utf-8 -*-
###################################################
# Manage all of the game status here              #
# "Screen" must be an intance og kivy Screen      #
###################################################
from globals import *
from subgames import *
from dialog_utils import *
from UI_utils import *
#from manager.update_manager import *

class ImageButton(ButtonBehavior, Image): #Behavior
	def __init__(self, callback,object_id=-1, **kargs):
		super(ImageButton, self).__init__( **kargs)
		self.callback = callback
		self.object_id = object_id#use this if it is an object
	def on_press(self):
		print('ImageButton on_press')
		self.callback()#self

turns = {1:2,2:3,3:0,0:1}
class GameManagerScreen(Screen):#main control class of the whole game
	#TODO: 自動存檔功能及記錄檔 防止意外關閉遊戲
	#TODO: Exceptions
	#TODO: 用計時器跟體力控制做出不同難度模式，預設為easy，不限時
	p0 = ObjectProperty()
	p1 = ObjectProperty()
	p2 = ObjectProperty()
	p3 = ObjectProperty()#can't bind Object if property changed?
	players = ReferenceListProperty(p0,p1,p2,p3)
	#reload_item_list = BooleanProperty(False)	
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
		#self.Chapters = self.init_chapters()
		self.object_table = self.load_object_table()
		self.unlock_table = self.load_unlock_table()
		self.synthesis_table = self.load_synthesis_table()
		self.name_to_id_table = self.load_name_to_id_table() #有些不同id的名稱會重複，重複時查總表
		self.NPC_table = self.load_NPC_table()

		print("global_w,global_h:",global_w,global_h)


	def link_main_screen(self):
		self.main_screen = self.manager.get_screen('story')
		self.Chapters = self.init_chapters(self.main_screen)

		#for testing
		j = 0
		c = 0
		for i in range(4):
			
			for str_id in self.object_table.keys():
				item = self.object_table[str_id]
				if item['source'] is not None:				
					self.players[i].item_list.append(int(str_id))#for testing
					c += 1
					if c>=4:
						break
			c = 0			
			self.players[i].GG = True

		self.main_screen.start_story(self)		

	def start_chapter(self):
		self.Chapters[self.current_player_id][self.current_chapter[self.current_player_id]].started = True

	def change_turn(self):
		print('turns:',turns)
		print('self.current_chapter:',self.current_chapter)
		if len(turns) == 0:
			self.to_ending(self.current_player_id)
		
		self.current_player_id = turns[self.current_player_id]
		return self.current_player_id, self.current_chapter[self.current_player_id] #(self.current_player_id, self.current_chapter[self.current_player_id])	

	def change_chapter(self):
		if self.current_chapter[self.current_player_id] == final_chapter:
			self.players[self.current_player_id].GG = True
			self.to_ending(self.current_player_id)
			self.exclude_from_turns(self.current_player_id)#set current_player_id to last player, for the change_turn
			
		else:
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

	def to_ending(self, player_id):
		last_one = False
		if self.p0.GG and self.p1.GG and self.p2.GG and self.p3.GG:
			last_one = True
		self.manager.get_screen('ending').load_ending(player_id,last_one)
		self.manager.current = 'ending'

	def init_chapters(self,main_screen): #TODO: load game info
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
			#print('load json object table:',table)
	
		return table

	def	load_unlock_table(self):
		with open('res/objects/unlock_table.json','r') as f:
			table = json.load(f)
		return table 

	def load_synthesis_table(self):
		with open('res/objects/synthesis_table.json','r') as f:
			table = json.load(f)
		return table 	

	def load_name_to_id_table(self):
		with open('res/objects/name_to_id_table.json','r') as f:
			table = json.load(f)
		return table 	

	def load_NPC_table(self):
		table = {0:{'name':'艾爾莎','source':'res/images/testing/Erza.png','map_name':'','pos_hint':'','size_hint':'','player':1,'chapter':0,'function_types':'','description':'妖精的尾巴'}}##key:NPC_id,value:(name,source,location,pos,player,chapter,function_types,description)		return table		
		return table
	#TODO: the function of auto save/load game status

	def load_game(self):
		f = open('res/game_archive.json','r')
		record_json = json.load(f)
		#current_player, 
		
	def save_game(self):
		f = open('res/game_archive.json','w')
		#TODO



class Player(object):#player_id=player_id
	def __init__(self, player_id, GM):
		self.GM = GM
		self.name = ''
		self.personality = ''
		self.item_list= []#only int key
		self.achievement = []
		#self.load_objects_table()
		self.load_personal_info(player_id)
		self.GG = False
	def get_item(self, object_id):#need to consider number of item?
		if object_id not in self.item_list:
			print('get_item:',object_id)
			self.item_list.append(object_id)#key:object_id,value:(name,source,location,pos,player,chapter,function_types,description)
			self.GM.manager.get_screen('story').reload_item_list = True 
		else:
			print('[*]Exception! Cannot get an item again!')
	def spend_item(self, object_id):
		if object_id in self.item_list:
			print('spend_item:',object_id)
			self.item_list.remove(object_id)#key:object_id,value:(name,source,location,pos,player,chapter,function_types,description)
			self.GM.manager.get_screen('story').reload_item_list = True 
		else:
			print('[*]Exception! Cannot spend an item that not in item list!')
	def get_achievement(self,achievement):
		pass #TODO:思考內容要放啥

	# def load_objects_table(self):
	# 	path = 'res/objects/'
	# 	#TODO
	def load_personal_info(self,player_id):
		path = 'res/players/'
		#needed??

class Chapter(object):
	def __init__(self, player_id, chapter_id,main_screen):
		self.object_path = f'res/chapters/{player_id}_{chapter_id}/objects/' #including a json and object images
		self.map_path = f'res/chapters/{player_id}_{chapter_id}/maps/'  #including map images
		self.dialog_path = f'res/chapters/{player_id}_{chapter_id}/dialogs/' #including two txt files
		self.scene_path = f'res/chapters/{player_id}_{chapter_id}/scenes/' #including scene images for the plot mode
		self.locked_map_path = 'res/images/locked/'
		self.player_chapter = (player_id,chapter_id)
		self.chapter_NPCs = [] #deprecated
		self.chapter_maps = self.add_chapter_maps()
		self.chapter_default_map = self.load_default_map(player_id, chapter_id)
		self.chapter_objects = self.load_chapter_objects_of_maps(main_screen) #objects_allocation[current_map] = list of MapObjects 
		#self.picked_item = []
		self.chapter_plot_scenes = self.load_plot_scenes()
		self.chapter_scenes_table = self.load_scenes_table()
		self.chapter_title = self.load_chapter_title(player_id, chapter_id)
		self.chapter_pre_plot, self.chapter_plot = self.load_chapter_dialogs()#self.chapter_predialog,self.chapter_postdialog
		self.started = False
		self.used_list = []#used objects' id

	def unlock_new_map(self,map_name):#DEBUG: 不需要重新載入所有地圖物件
		for locked_img in os.listdir(self.locked_map_path):
			if map_name in locked_img:
				self.chapter_maps.append(os.path.join(self.locked_map_path,locked_img))
				break
		#TODO
		self.load_chapter_objects_of_maps(main_screen)#load new objects info of unlocked map

	def load_default_map(self,player_id, chapter_id):
		# if (player_id==1 and chapter_id==2) or (player_id==2 and chapter_id==1):
		# 	return -1 #TODO

		default_maps = ['雙人宿舍夜','博雅','雙人宿舍日','雙人宿舍日','農場夜',\
		'B男宿舍夜','排球場','女主家裡房間一','女主家C男房間晚一','女主家C男房間晚一','女主家客廳',\
		'女主家C男房間晚二','D女房間','D女房間','D女房間二','D女房間二']
		# default_map = [[],[],[],[]]
		for i,m in enumerate(self.chapter_maps):
			if default_maps[player_id*4+chapter_id] in m:
				return i
		return 0
	def load_chapter_dialogs(self):#TODO: read ine of those 16 file

		# max1 = 0
		f1 = open(os.path.join(self.dialog_path,'1.txt'),'r',encoding='utf-16')		
		pre =[line for line in f1.read().split('\n') if len(line)>0]
		part1 = []
		for line in pre:
			line_list = line.split(':')
			if len(line_list)>1:
				part1.append([line_list[0],line_list[1]])
				# if len(line_list[1]) > max1:
				# 	max1 = len(line_list[1])
			else:
				part1.append(['',line])
				# if len(line) > max1:
				# 	max1 = len(line)

		# max2 = 0
		f2 = open(os.path.join(self.dialog_path,'2.txt'),'r',encoding='utf-16')
		post = [line for line in f2.read().split('\n') if len(line)>0]
		part2 = []
		for line in post:
			line_list = line.split(':')
			if len(line_list)>1:
				part2.append([line_list[0],line_list[1]])
				# if len(line_list[1]) > max2:
				# 	max2 = len(line_list[1])
				# 	print('max line:',line_list[1])
			else:
				part2.append(['',line])
				# if len(line) > max2:
				# 	max2 = len(line)
				# 	print('max line:',line)
		#print('part2:',part2)
		#print(f'Line length MAX1:{max1},MAX2:{max2}')
		return part1,part2#can be many dialog_parts?
	def load_chapter_title(self,player_id, chapter_id):
		text = ['紊亂的書房','曾經的約定','妹妹的男友','隱藏的崇拜','蒼白的生日','錯位的戀情','青鳥的囚籠','友誼的裂痕','超載的負荷','哭泣的卡片','哭泣的女孩','紀念的贈禮','手機的密碼','補全的卡片','渴望的支持','遺失的過往'][4*chapter_id+player_id]
		return Label(text=text,color=(1,1,1,1),pos_hint={'x':.25,'y':.4},size_hint=(.5,.3),halign='center',valign='center',font_size=184,font_name='res/HuaKangTiFan-CuTi-1.otf')
	def load_chapter_objects_of_maps(self,main_screen):
		#TODO: load and init all MapObject here in existing map
		#from self.object_path 
		maps = self.chapter_maps
		chapter_objects = []
		for i in range(len(maps)):
			chapter_objects.append([])

		with open(self.object_path+'chapter_objects.json','r') as f:
			objects_table = json.load(f)
			#print('chapter\'s objects_table:',objects_table)
			for str_id in  objects_table.keys():
				obj = objects_table[str_id]
				if obj['on_map_name'] is not None:
					if obj['pos_hint'] is not None and obj['size_hint'] is not None:
						on_map = 0
						for map_id,map_path in enumerate(maps):
							#print('obj[\'on_map_name\']:',obj['on_map_name'])
							#print('map_path...:',map_path.split('/')[-1].split('.')[0])
							if obj['on_map_name'] == map_path.split('/')[-1].split('.')[0]:
								print(f'map id:{map_id} allocate object id:{str_id}')
								chapter_objects[map_id].append(MapObject(screen=main_screen, object_id=int(str_id),object_content=obj,\
								size_hint=obj['size_hint'],pos_hint={'x':obj['pos_hint'][0],'y':obj['pos_hint'][1]}))
								on_map = 1
								break
						if not on_map:
							print(f'[*] Exception! Can\'t find object:{obj}\'s map!')

					else:
						print(f'[*] Exception! object:{obj} 資料不足') 

		# MapObject
		print('chapter_objects:',chapter_objects)
		return chapter_objects
	
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

	def add_chapter_maps(self):

		chapter_maps = []
		for f in os.listdir(self.map_path):
			if '.jpg' in f or '.png' in f:
				chapter_maps.append(os.path.join(self.map_path,f))
		print('chapter_maps:',chapter_maps)
		return chapter_maps


	def add_chapter_NPCs(self,NPC_id):
		#TODO: load and init all MapObject here
		self.chapter_NPCs.append(NPC_id)
		#return chapter_NPCs

	def get_NPCimage_path(self):
		#TODO: load NPC images
		return 'res/images/testing/Erza.png'


class MapObject(Widget):#ImageButton):#TODO:或是只繼承ButtonBehavior 然後用canvas區分是否有source圖片
	def __init__(self,object_id,object_content,screen,touch_range='default', **kargs):
		#依照是否有source圖片區分
		#self.callback = partial(self.probe_object_on_map,self,screen)#()
		super(MapObject, self).__init__(**kargs)
		self.object_id = object_id
		self.source = object_content['source']
		#super(MapObject, self).__init__(self.callback,self.object_id,allow_stretch=True,keep_ratio=False,**kargs)
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
			self.canvas.add(Rectangle(source=self.source,pos=(self.pos_hint['x']*global_w,self.pos_hint['y']*global_h),\
				size=(self.size_hint[0]*global_w,self.size_hint[1]*global_h),group='mapobject'))

		if touch_range == 'default':
			self.touch_range = self.size_hint
		else:
			self.touch_range = touch_range

	def on_touch_down(self,touch):
		print(f"Map object on_touch_down touch.pos:{touch.pos}")
		if self.collide_point(*touch.pos):
			self.probe_object_on_map()

	def probe_object_on_map(self,*args):
		print(f'self:{self},args:{args}')
		screen = self.screen#args[1]
		
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