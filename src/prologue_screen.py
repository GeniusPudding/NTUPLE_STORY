###################################################
# Prologue appeared before the main screen        #
###################################################
from game_manager import *

class PrologueScreen(Screen):
	w = NumericProperty()
	h = NumericProperty() 
	dialogframe_width = NumericProperty(0.85)	
	dialogframe_height = NumericProperty(0.2)
	start_autoplay = BooleanProperty(False)
	finish_auto = BooleanProperty(False)
	current_speaker_name = StringProperty()
	dialog_events = ListProperty()
	nametag = ObjectProperty(Label())
	def __init__(self, **kwargs):
		super(PrologueScreen, self).__init__(**kwargs)
		self.size = (self.w,self.h) = (global_w,global_h) 

		self.auto_dialog = [[speaker_name[line.split(':')[0]],line.split(':')[1]] for line in 'N:那是個普通的日子。\n\
N:普通的校區、普通的椰林、普通的總圖。\n\
N:一場，再普通不過的太陽雨。\n\
N:雨停之後，她再也沒出現。\n\
C:(憤怒的拍桌)X去哪裡了！你們真一點想法也沒有？\n\
D:(白眼)你兇有什麼用？能解決問題嗎？\n\
C:(怒吼)失蹤的不是你妹妹！你懂什麼！我醜話先說在前頭，要是X有個萬一，我就是...\n\
A:(害怕)你...你們別吵了，X她...\n\
C:(怒瞪A一眼)\n\
B:(興致缺缺的移開視線，彷彿事不關己)人沒了就是沒了，急有什麼用。\n\
C:(憤怒的揪起B的衣領)你說得這是人話嗎！要不是你、我妹妹怎麼會消失！\n\
B:(一臉莫名其妙)我？ (翻白眼，但眼神中透著心虛)你別瘋狗亂咬人，X跟我明明白白，我們一點問題都沒有。\n\
C:(聽了B的話愣了好一陣子，臉上寫滿了不敢置信，眼神隨即變得兇惡)你有膽再說一次！\n\
C:A！妳說過我家X這些時間都不對勁是吧？有這麼回事吧？\n\
A:(被嚇了一跳，唯唯諾諾的點頭，眼神飄移著)X...X她的確...\n\
C:還有D！上回你們見面又發生了什麼事？\n\
D:(滿臉莫名其妙，一臉看瘋子似的眼神)從頭到我到底關我什麼事？我和X已經多少年沒見面了！\n\
D:不過我說，你從頭到尾到底在亂吼些什麼？那是你妹妹，你自己不該最清楚嗎？\n\
C:(面色突然的僵硬，眼神中帶著哀傷)...我不知道。\n\
N:會議室內被突如其來的沉默籠罩，所有人互看著，各異的眼神打轉各自的心思，\n\
N:X的失蹤彷彿一根刺，梗在所有人的喉間，呼吸變得困難，近乎溺水的窒息感讓人喘不過氣，\n\
N:但最終誰也無法在這片泥沼中待著，D面色厭煩地離開了會議室，接著所有人魚貫而出，似乎不願再正視這麼件事。\n\
N:只是，X的失蹤彷彿夢魘一般，在每個人的心頭盤據。\n\
N:所有人都還沒注意到，自己曾經的一舉一動，都在另一人心上畫下傷痕，\n\
N:那個人每天每夜對著淌血的傷口無助的嘆息，最終走向漠視。'.split('\n')]
		replaced = []
		for line in self.auto_dialog:
			name = line[0]
			dialog = line[1]
			for k in speaker_name.keys():
				dialog = dialog.replace(k,speaker_name[k])
			replaced.append([name,dialog])

		self.auto_dialog = replaced	
		#print('self.auto_dialog:',self.auto_dialog)
		Window.bind(on_key_down=self.key_action)
		self.bind(start_autoplay=partial(auto_play_dialog,self,self.auto_dialog))
		self.bind(current_speaker_name=partial(auto_display_speaker,self))
		self.bind(finish_auto=partial(auto_prompt,self,'Enter',{'x':.25,'y':.4}))
		self.displaying_character_labels = []
		#self.nametag = Label()	

	def key_action(self, *args):
		if self.manager.current == 'prologue':	
			print('key: ',args)
			press_key_id = args[1]#args[1]:ASCII?

			if press_key_id == 13:
				print('start_autoplay:',self.start_autoplay)
				if not self.start_autoplay:
					print('get enter 1')
					self.clear_seal()
					#return

			#elif press_key_id == 110:#n:
				elif self.finish_auto:
					print('Go to story')
					# print('self.manager.get_screen(\'story\').seal_on:',self.manager.get_screen('story').seal_on)
					# print('self.manager.get_screen(\'story\').current_mode:',self.manager.get_screen('story').current_mode)
					self.remove_widget(self.prompt_label)
					self.manager.get_screen('story').seal_on = False
					self.manager.current = 'story' #'seal'# 'story' 
					self.manager.get_screen('story').seal_on = True
					
					# print('self.manager.get_screen(\'story\').seal_on:',self.manager.get_screen('story').seal_on)
					#return
			#for testing
			elif press_key_id == 115:#s
				if self.start_autoplay: 
					print('Skip the auto dialog')
					for event in self.dialog_events:
						event.cancel()
					clear_displayed_text(self,self.displaying_character_labels)
					self.finish_auto = True
			return True
	def on_touch_down(self,touch):	
		if not self.start_autoplay:
			self.clear_seal()
	def clear_seal(self):
		self.canvas.remove_group('seal')
		self.clear_widgets()
		self.start_autoplay = True