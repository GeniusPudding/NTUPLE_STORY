from game_manager import *

#TODO: subgames import game_manager
class SubgameManager(Screen):
	def __init__(self, **kwargs):
		super(SubgameManager, self).__init__(**kwargs)
		self.subgames = [MazeGame(name='maze'), PuzzleGame(name='puzzle')] #append all subgame instance here
		self.cur_subgames_id = -1
		self.w, self.h = global_w,global_h#= get_screen_size()
		#self.leave_button = ImageButton(callback=self.leave_subgames,source='res/images/testing/exit.png',pos=(.1*self.w,.1*self.h),size=(.2*min(self.w, self.h),.2*min(self.w, self.h)),size_hint = (None,None))
		self.initialized = False #
		# for subgame in self.subgames:
		# 	subgame.add_widget(self.leave_button)
		# 	self.manager.add_widget(subgame)	#when SubgameManager.__init__(), self.manager is still None
	def init_all_subgames(self):#after the self.manager built 
		print('init all subgames')
		for subgame in self.subgames:
			self.leave_button = ImageButton(callback=self.leave_subgames,source='res/images/testing/exit.png',pos_hint={'x':.1,'y':.1},size_hint=(.2*min(self.w, self.h)/self.w,.2*min(self.w, self.h)/self.h))
			subgame.add_widget(self.leave_button)
			self.manager.add_widget(subgame)
		self.initialized = True
	def start_subgame_id(self, subgames_id):
		self.cur_subgames_id = subgames_id
		
		# self.subgames[subgames_id].add_widget(self.leave_button)
		# subgame = self.subgames[subgames_id]
		# self.manager.add_widget(subgame)
		print('loading self.manager:',self.manager)
		self.subgames[subgames_id].start()
		self.manager.current = self.subgames[subgames_id].name
		

	def leave_subgames(self,btn):
		# self.manager.get_screen('story').generate_dropdown()
		self.subgames[self.cur_subgames_id].end()
		self.manager.current = 'story'
		self.cur_subgames_id = -1
	#display background,item's image, and item's info 

class TestApp(App):
	def build(self):
		game = SubgameManager(name='subgames_manager')#??
		game.load_subgame(MazeGame())
  		
		return game

if __name__ == '__main__':


    TestApp().run()


