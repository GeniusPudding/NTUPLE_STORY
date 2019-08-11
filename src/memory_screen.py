from game_manager import *

class MemoryScreen(Screen):

	def __init__(self, **kwargs):
		super(MemoryScreen, self).__init__(**kwargs)


	def load_memory(self, player_id, chapter_id):
		pass

	def back_to_story(self):#next chapter?
		self.manager.current = 'story'