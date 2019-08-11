from game_manager import *
class InfoScreen(Screen):
	#personal info 
	def __init__(self, **kwargs):
		super(InfoScreen, self).__init__(**kwargs)

	def back_to_plot(self):
		#self.manager.get_screen('story').
		self.manager.current = 'story' 	   