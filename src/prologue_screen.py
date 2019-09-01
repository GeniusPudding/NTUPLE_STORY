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
	current_line = StringProperty('')
	current_char_id = NumericProperty(0)
	display_pausing = NumericProperty(0)#0:not in auto dialog, 1:auto displaying, 2: auto pausing

	def __init__(self, **kwargs):
		super(PrologueScreen, self).__init__(**kwargs)
		self.size = (self.w,self.h) = (global_w,global_h) 
		self.prompt_label = Label()

		f = open('res/dialogs/第零章.txt','r',encoding='utf-16')#,encoding='utf-8')
		r = f.read()

		self.auto_dialog = []
		for line in r.split('\n'):
			if len(line) == 0:
				continue
			if len(line.split(':')) > 1:
				self.auto_dialog.append([line.split(':')[0],line.split(':')[1]])
			else:
				self.auto_dialog.append(['N',line])
		print('self.auto_dialog:',self.auto_dialog)

		#auto_prompt(self,'Enter',{'x':.2,'y':.3},instance=self, prompt=True,pre_info='故事開始',post_info='')
		Window.bind(on_key_down=self.key_action)
		self.bind(start_autoplay=partial(auto_play_dialog,self,self.auto_dialog))
		self.bind(current_speaker_name=partial(auto_display_speaker,self))
		self.bind(finish_auto=partial(auto_prompt,self,'Enter',{'x':.2,'y':.3},pre_info='一切 就是如此倉促...',post_info='翻開這本\n再也闔不上的\n現實'))
		self.displaying_character_labels = []

	def key_action(self, *args):
		if self.manager.current == 'prologue':	
			print('key: ',args)
			press_key_id = args[1]

			if press_key_id == 13:
				print('start_autoplay:',self.start_autoplay)
				if not self.start_autoplay:
					print('get enter 1')
					self.clear_seal()

				elif self.finish_auto:
					print('Go to story')
					self.remove_widget(self.prompt_label)
					self.manager.get_screen('story').seal_on = False
					self.manager.current = 'story' #'seal'# 'story' 
					self.manager.get_screen('story').seal_on = True
					
			elif press_key_id == 112:#p
				if self.start_autoplay and not self.finish_auto:
					if self.display_pausing == 1:
						auto_pause(self,pre_info='猶豫了嗎...')
						# print('Pause the auto dialog')
						# #self.clear_text_on_screen()
						# cancel_events(self)
						# print('pausing self.displaying_character_labels:',self.displaying_character_labels)
						# s = ''
						# for l in self.displaying_character_labels[:self.current_char_id+1]:
						# 	s += l.text
						# print('pausing s:',s)
						# print('pausing self.auto_dialog:',self.auto_dialog)

						# auto_prompt(self,'r',{'x':.2,'y':.3},instance=self, prompt=True,pre_info='猶豫了嗎...',post_info='再次面對人生')						
						# Clock.schedule_once(partial(pause,self),1.2) 

					#elif self.display_pausing == 2:
			elif press_key_id == 114:#r
				if self.start_autoplay and not self.finish_auto:
					if self.display_pausing == 2:
						auto_continue(self)
						# self.remove_widget(self.prompt_label)
						# s = ''
						# for l in self.displaying_character_labels[self.current_char_id+1:]:
						# 	s += l.text
						# #先跑完該句剩下的
						# s_time,c_time,n_time = read_velocity_config()
						# res_time = display_character_labels(self,s,s_time,n_time,c_time,restart_id=self.current_char_id+1)
						# #再重新開始播放動畫
						# self.auto_dialog = self.auto_dialog[self.auto_line_id+1:]
						# Clock.schedule_once(partial(auto_play_dialog,self,self.auto_dialog),res_time)#self.display_pausing = 1	

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