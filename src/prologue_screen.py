###################################################
# The prologue displayed before the main story    #
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
	current_player_id = NumericProperty(-1)#for auto dialog
	current_chapter = NumericProperty(-1)
	def __init__(self, **kwargs):
		super(PrologueScreen, self).__init__(**kwargs)
		self.size = (self.w,self.h) = (global_w,global_h) 

		f = open('res/dialogs/第零章.txt','r',encoding='utf-16')#,encoding='utf-8')
		r = f.read()


# 		self.auto_dialog = [[line.split(':')[0],line.split(':')[1]] for line in 'N:——西元2029年，十月——\n\
# N:——某國立大學孟姓女大生失蹤——\n\
# N:——據可靠消息來源，該女大生於去年入學該國立大學——\n\
# 孟亦寒_生氣:我妹妹孟亦安去哪裡了！你們真一點想法也沒有？\n\
# 亓官楓_無表情:你兇有什麼用？能解決問題嗎？\n\
# 李語蝶_難過:你...你們別吵了，亦安她...\n\
# 司馬熏_無表情:人沒了就是沒了，急有什麼用。\n\
# 孟亦寒_生氣:（憤怒的揪起司馬熏的衣領）你說得這是人話嗎！你不是她的男友嗎？要不是你，我妹妹怎麼會消失！\n\
# 司馬熏_小意外:我？亦安跟我明明白白，我們一點問題都沒有。\n\
# 孟亦寒_生氣:李語蝶！妳是亦安的室友，說過我家亦安這些時間都不對勁是吧？有這麼回事吧？\n\
# 李語蝶_難過:孟亦安...孟亦安她的確...\n\
# 孟亦寒_生氣:還有亓官楓！你們不是高中好閨密嗎？\n\
# 亓官楓_無表情:我說，你從頭到尾到底在亂吼些什麼？那是你妹妹，你自己不該最清楚嗎？\n\
# 孟亦寒_不知所措:我...我不知道。\n\
# N:孟亦安的失蹤彷彿夢魘一般，在每個人的心頭盤據。\n\
# N:孟亦安，真的失蹤了。'.split('\n')]

		#self.auto_dialog = [[line.split(':')[0],line.split(':')[1]] for line in r.split('\n')]
		self.auto_dialog = []
		for line in r.split('\n'):
			if len(line) == 0:
				continue
			if len(line.split(':')) > 1:
				self.auto_dialog.append([line.split(':')[0],line.split(':')[1]])
			else:
				self.auto_dialog.append(['N',line])
		print('self.auto_dialog:',self.auto_dialog)

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