from game_manager import *

class SealScreen(Screen):
	title = StringProperty()
	def __init__(self, **kwargs):
		super(SealScreen, self).__init__(**kwargs)
		Window.bind(on_key_down=self.key_action)
	def load_title(self,title):
		self.title = title
		print('self.title :',self.title )
	def key_action(self, *args):
		
		if self.manager.current == 'seal':	
			print('test seal key: ',args)
			press_key_id = args[1]
			if press_key_id == 110:
				self.manager.current = 'story'

	def on_touch_down(self,touch):
		self.manager.current = 'story'