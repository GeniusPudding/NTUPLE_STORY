from game_manager import *
class CoverScreen(Screen):
	def __init__(self, **kwargs):
		super(CoverScreen, self).__init__(**kwargs)
		Window.bind(on_key_down=self.key_action)
	def key_action(self, *args):
		if self.manager.current == 'title':	#DEBUG:收不到
			print('Title args:',args)
			press_key_id = args[1]
			print("press_key_id:",press_key_id)
			if press_key_id == 13:
				self.manager.current = 'intro'
			return True

	def on_touch_down(self, touch):
		self.manager.current = 'intro'