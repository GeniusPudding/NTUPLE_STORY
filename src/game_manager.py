# -*- coding: utf-8 -*-
###################################################
# Manage all of the game status here              #
# "Screen" must be an intance og kivy Screen      #
###################################################


from globals import *
from subgames import *
from dialog_utils import *
from UI_utils import *
#import pandas as pd



#from manager.update_manager import *

#TODO: 區分GM和主畫面之所屬功能




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
		#self.players = [Player(player_id) for player_id in range(4)]
		self.players_name = {0:'室友',1:'男友',2:'哥哥',3:'故人'}
		self.Chapters = self.init_chapters()
		self.object_table = self.load_object_table()
		self.unlock_table = self.load_unlock_table()
		self.NPC_table = self.load_NPC_table()
		#self.testing_set_chapters_contents(self.object_table, self.NPC_table)
		
		print("global_w,global_h:",global_w,global_h)

		#self.bind(reload_item_list=self.auto_instant_update)

	#非當前螢幕所以不產生事件??
	# def auto_instant_update(self, instance, reload_item_list ):
	# 	print('[*] auto update:',instance)
	# 	if reload_item_list and self.manager.get_screen('story').itemframe is not None:
	# 		self.manager.get_screen('story').itemframe.item_list = self.players[self.current_player_id].item_list	
	# 		self.reload_item_list = False


	def link_main_screen(self):
		self.main_screen = self.manager.get_screen('story')

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
		# Clock.schedule_interval(global_mouse, 0.6)	
		#self.players[i]
		
	def change_turn(self):
		print('turns:',turns)
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
	# def init_players(self): #TODO
	# 	for p in range(1,5):
	# 		self.players.append(Player(player_id=p)) 
	def init_chapters(self): #TODO: load game info
		Chapters = []
		for p in range(4):
			Chapters.append([])
			for r in range(4):
				Chapters[p].append(Chapter(player_id=p, chapter_id=r))
		return Chapters
	def load_object_table(self):
		#'id':{'name','source','map_name','pos_hint','size_hint','player','chapter','function_types','description','on_map'}
		with open('res/objects/final_objects_table.json','r') as f:
			table = json.load(f)
			#print('load json object table:',table)
		
		return table

	def	load_unlock_table(self):
		with open('res/objects/unlock_table.json','r') as f:
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
		print('get_item:',object_id)
		self.item_list.append(object_id)#key:object_id,value:(name,source,location,pos,player,chapter,function_types,description)
		self.GM.manager.get_screen('story').reload_item_list = True 
	def use_item(self, object_id):
		self.item_list.remove(object_id)#key:object_id,value:(name,source,location,pos,player,chapter,function_types,description)
		self.GM.manager.get_screen('story').reload_item_list = True 
	def get_achievement(self,achievement):
		pass #TODO:思考內容要放啥

	# def load_objects_table(self):
	# 	path = 'res/objects/'
	# 	#TODO
	def load_personal_info(self,player_id):
		path = 'res/players/'
		#needed??

class Chapter(object):
	def __init__(self, player_id, chapter_id):
		self.object_path = f'res/chapters/{player_id}_{chapter_id}/objects/' #including a json and object images
		self.map_path = f'res/chapters/{player_id}_{chapter_id}/maps/'  #including map images
		self.dialog_path = f'res/chapters/{player_id}_{chapter_id}/dialogs/' #including two txt files
		self.player_chapter = (player_id,chapter_id)#(player,chapter)
		self.chapter_NPCs = [] 
		self.chapter_maps = self.add_chapter_maps(player_id, chapter_id)
		self.chapter_objects = []#load_chapter_objects()  
		self.started = False
		self.chapter_title = self.load_chapter_title(player_id, chapter_id)
		self.pre_plot, self.plot = self.load_chapter_dialogs(player_id, chapter_id)#self.chapter_predialog,self.chapter_postdialog

	def load_chapter_dialogs(self,player_id, chapter_id):#TODO
		# with open(self.dialog_path+'pre.txt','r') as f:
		# 	r = f.read()
		# 	dialog_part = [[line.split(':')[0],line.split(':')[1]] for line in r]
		# with open(self.dialog_path+'post.txt','r') as f:
		# 	r = f.read()	
		# 	dialog_part2 = [[line.split(':')[0],line.split(':')[1]] for line in r]		
		#for testing
		dialog_part = [[line.split(':')[0],line.split(':')[1]] for line in 'N:(房門關閉聲)\n\
N:一場不歡而散的會議後，A回到屬於自己和X的宿舍，盤踞心頭的愁雲和窒息感卻沒應此而減少，反而在一片寂靜中無聲的滋長。\n\
A:(關上門後無助的沿著門板跌坐在地，把臉埋在臂彎之間)不是我的錯，這和我無關，和我一點關係也沒有！\n\
N:C憤怒而受傷的神色揮之不去，濃厚的罪惡感在思緒中揮舞著利爪，思考變得破碎，始終無法連貫，\n\
N:但怎麼想，C也想不出來自己做錯了些什麼。\n\
N:所以，不是我的錯。\n\
N:原本是這麼想著，A才稍稍緩下情緒，卻瞥見了書桌上的一件物品，表情一瞬間的慘白，彷彿想起了些什麼，\n\
N:胸口被人緊掐著，連呼吸都是折磨。'.split('\n')]
		
		dialog_part2 = [[line.split(':')[0],line.split(':')[1]] for line in 'B:欸，怎麼了？一副愁雲慘霧的？\n\
X:(拿著成績單，表情難過得快哭出來似的)B...怎麼辦啦，我的模考成績...\n\
B:(表情疑惑地接過成績單，臉上一瞬間的錯愕)老天，這怎麼回事？不是說這次有妳哥哥幫妳嗎？怎麼整整掉了三個級分？\n\
X:(表情難過的欲言又止，最終只是搖頭)我不知道...我回家之後要怎麼辦...\n\
N:一想起回家後可能發生的畫面，X忍不住哽咽，B看著心裡也難過，煩躁地抓亂了頭髮，卻無能為力，只能好言安慰了一番，最終X神色失落的回到家，顫抖著手遞出了成績單。\n\
F:(看了一眼成績單，憤怒的拍在桌上)這種成績也敢拿回家丟人現眼！\n\
X:(害怕得發抖)我...我...我不是...\n\
M:(無奈地嘆氣，拍拍F的肩膀)別對X生氣，考這種成績也不是她願意的...\n\
N:聽了M這麼緩和氣氛，X才稍稍鬆了口氣，下一句話，心情卻被一瞬間的推落懸崖，不斷的，向無底的深淵跌落。\n\
M:(嘆氣)X沒有她哥哥那麼聰明，稍微笨了一點，何必強迫孩子？\n\
N:一句話深深刺傷X所剩無幾的自尊，也許是人生中第一次，手臂一揮，掃落了桌上的杯具，X無視瓷器碎裂的聲音和父親的怒吼，逃入房中上了鎖，再也不願意開門。\n\
N:而客廳裡，作為哥哥的C卻承擔了父母所有的怒火。\n\
F:你看看你妹妹那是什麼德性！就告訴你不要跟她玩在一起，她這年紀就該念書！你跟她說什麼遊戲，談什麼動畫！\n\
M:(難過地擦眼淚)就是啊，C...你也不想想，要是你妹妹怎麼了，到時候難過的還是你啊...\n\
N:C沈默著，對所有的指責和訓話保持緘默，似乎已經放棄了爭辯。\n\
N:也許，從那一刻起，很多事情就已經扭曲了。'.split('\n')]

		return dialog_part,dialog_part2#can be many dialog_parts?
	def load_chapter_title(self,player_id, chapter_id):
		return ['紊亂的書房','曾經的約定','妹妹的男友','隱藏的崇拜','蒼白的生日','錯位的戀情','青鳥的囚籠','友誼的裂痕','超載的負荷','哭泣的卡片','哭泣的女孩','紀念的贈禮','手機的密碼','補全的卡片','渴望的支持','遺失的過往'][4*chapter_id+player_id]

	def load_chapter_objects(self):
		#TODO: load and init all MapObject here
		with open(self.object_path+'object.json','r') as f:
			data_dict = json.load(f)
		# MapObject
		# self.chapter_objects.append(object_id)
		
	def add_chapter_maps(self,player_id, chapter_id):

		chapter_maps = []
		for f in os.listdir(self.map_path):
			if '.jpg' in f or '.png' in f:
				print(f'player_id:{player_id}, chapter_id:{chapter_id}, f:{f}')
				chapter_maps.append(os.path.join(self.map_path,f))
		#for testing
		# chapter_maps.append('res/images/screens/testing/'+str(player_id+1)+'_'+str(chapter_id+1)+'_1.jpg')
		# chapter_maps.append('res/images/screens/testing/'+str(player_id+1)+'_'+str(chapter_id+1)+'_2.jpg')
		# chapter_maps.append('res/images/screens/testing/'+str(player_id+1)+'_'+str(chapter_id+1)+'_3.jpg')
		return chapter_maps
	def add_chapter_NPCs(self,NPC_id):
		#TODO: load and init all MapObject here
		self.chapter_NPCs.append(NPC_id)
		#return chapter_NPCs

	def get_NPCimage_path(self):
		#TODO: load NPC images
		return 'res/images/testing/Erza.png'


class MapObject(ImageButton):# 有可能會改成繼承FreeDraggableItem的ImageButton 
	def __init__(self,object_id,object_content,screen,touch_range , **kargs):
		#Window.bind(on_key_down=self.key_action)
		#self.source = 'res/images/testing/synthesisframe.png'
		self.callback = partial(self.probe_object_on_map,self,screen)#()
		self.object_id = object_id
		super(MapObject, self).__init__(self.callback,self.object_id,**kargs )
		self.object_content = object_content
		self.object_types = object_content['function_types']
		self.map_name = object_content['map_name']
		self.source = object_content['source']
		#screen = screen
		if touch_range == 'default':
			self.touch_range = self.size_hint
		else:
			self.touch_range = touch_range
		print('create object types:',self.object_types)
		#only five probable types, one or many of ['item','puzzle','synthesis','trigger','clue'] or 'nothing'

	def probe_object_on_map(self,*args):#, self
		print(f'self:{self},args:{args}')
		screen = args[1]
		print('equal:',self==args[0])
		if isinstance(self,MapObject) and screen.current_mode == 1 and screen.item_view == 0:
			if screen.hp_per_round > 0:
				if 'item' in self.object_types:
					#定義: 可以收進"道具欄"並可"使用"
					screen.on_press_item(self)
				else:
					if 'puzzle' in self.object_types:
						#定義: 物件需要輸入正確密碼，以打開該物件；例如[密碼鎖]
						screen.on_press_puzzle(self) 
					if 'lock' in self.object_types:
						#定義: 將正確道具拖曳至此物件，以打開該物件；例如[鑰匙]
						screen.on_press_lock(self) 
					if 'synthesis' in self.object_types:
						#定義: 將正確道具拖曳至此物件，以打開該物件；例如[鑰匙]
						screen.on_press_synthesis(self)
					if 'clue' in self.object_types:
						#定義: 作為［解碼］所需要的關鍵資訊
						screen.on_press_clue(self) 
					if 'trigger' in self.object_types:
						#定義: 點擊即觸發進入劇情
						screen.on_press_trigger(self) 
					if 'switching' in self.object_types:
						#定義: 點擊切換場景用
						screen.on_press_switching(self) 	
					if 'nothing' in self.object_types:
						screen.on_press_nothing(self) 	
				
				screen.hp_per_round -= 1
			else:
				print('No HP in this round')

	def puzzle_bg(self, source):
		path = source #TODO
		return path
 

def puzzle_jugde(screen,GM,puzzle_object_id):
	#TODO: 載入解碼表

	screen.puzzle_pass = True


#GM = GameManagerScreen()
#pygame.init()


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