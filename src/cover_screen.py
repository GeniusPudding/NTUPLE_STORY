from game_manager import *

class CoverScreen(Screen):
	new_game = StringProperty('[b]' + escape_markup('重獲 ☆ 新生') + '[/b]')
	load_game = StringProperty('[b]' + escape_markup('再續 ☆ 前緣') + '[/b]')	
	def __init__(self, **kwargs):
		super(CoverScreen, self).__init__(**kwargs)
		Window.bind(on_key_down=self.key_action)
		# sound = SoundLoader.load('res/login.mp4')
		# if sound:
		#     print("Sound found at %s" % sound.source)
		#     print("Sound is %.3f seconds" % sound.length)
		#     sound.play()
	def key_action(self, *args):
		if self.manager.current == 'cover':
			print('Cover args:',args)
			press_key_id = args[1]
			print("press_key_id:",press_key_id)
			if press_key_id == 13:
				self.manager.current = 'intro'

			return True

	def set_init_button(self):

		pass

	def on_press_new(self,btn):
		print('新遊戲!')
		self.manager.current = 'intro'
	def on_press_load(self,btn):	
		print('載入遊戲!')
		pickle_list = ['0_0.pickle','0_1.pickle','0_2.pickle','0_3.pickle',\
		'1_0.pickle','1_1.pickle','1_2.pickle','1_3.pickle',\
		'2_0.pickle','2_1.pickle','2_2.pickle','2_3.pickle',\
		'3_0.pickle','3_1.pickle','3_2.pickle','3_3.pickle',\
		'p0.pickle','p1.pickle','p2.pickle','p3.pickle','current_c_p.pickle','main_screen.pickle']
		pickle_path = 'res/pickles/'
		
		if set(pickle_list) - set(os.listdir(pickle_path)) != set():#缺少記錄檔
			print('載入遊戲失敗!')
			return
		self.manager.get_screen('story').seal_on = False
		self.manager.current = 'story'
		self.manager.get_screen('story').load_game()
		



	# def on_touch_down(self, touch):
	# 	self.manager.current = 'intro'
