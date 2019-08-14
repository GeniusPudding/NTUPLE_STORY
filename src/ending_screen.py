from game_manager import *


class EndingScreen(Screen):
    def __init__(self, **kwargs):
        super(EndingScreen, self).__init__(**kwargs)

    def load_ending(self, player_id,last_one):
    	print(f'Show {player_id+1}-th player\'s ending')
    	if last_one:
    		print('End The Story')

    #破關就刪掉存檔檔案