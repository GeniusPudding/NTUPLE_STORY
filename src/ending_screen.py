from game_manager import *


class EndingScreen(Screen):
    def __init__(self, **kwargs):
        super(EndingScreen, self).__init__(**kwargs)

    def load_ending(self):
    	#print(f'Show {player_id+1}-th player\'s ending')
    	#if last_one:
    	print('End The Story')
    	#TODO

    	pickle_path = 'res/pickles/'#破關就刪掉存檔檔案
    	for f in os.listdir(pickle_path):
    		if '.pickle' in f:
    			os.remove(os.path.join(pickle_path,f))

    