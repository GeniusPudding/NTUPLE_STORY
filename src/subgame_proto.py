from kivy.uix.screenmanager import Screen
class SubGame(Screen):
	def __init__(self, **kwargs):
		super(SubGame, self).__init__(**kwargs)
		self.name = ""
	def start(self):
			
		print("subgame start, need to load child class") 
	def reset_game(self):
		print("subgame reset, need to reset child class") 
	def end(self):
		print("subgame end, need to stop child class") 
