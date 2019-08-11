from game_manager import *
class TitleScreen(Screen):
	def __init__(self, **kwargs):
		super(TitleScreen, self).__init__(**kwargs)
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text2')
		self._keyboard.bind(on_key_down=self.key_action)
		#Window.bind(on_key_down=self.key_action)
	def key_action(self, *args):
		if self.manager.current == 'title':	
			print('Title args:',args)
			press_key_id = args[1][0]
			print("press_key_id:",press_key_id)
			if press_key_id == 13:
				self.manager.current = 'intro'
			return True
	def _keyboard_closed(self):
		print('My keyboard have been closed!')
		self._keyboard.unbind(on_key_down=self.key_action)
		self._keyboard = None

	def on_touch_down(self, touch):
		self.manager.current = 'intro'