###################################################
# Object screen for object allocating             #
###################################################
from game_manager import *

turns = {1:2,2:3,3:0,0:1}

class ObjectScreen(Screen):
	current_player_id = NumericProperty(1)
	current_chapter = NumericProperty(1)
	current_player_chapter = ReferenceListProperty(current_player_id, current_chapter)
	current_map = NumericProperty(-1)
	chapter_maps = ListProperty()
	def __init__(self, **kwargs):
		super(ObjectScreen, self).__init__(**kwargs)

	def start(self):

		self.bg_widget = BG_widget(parent =self)
		self.add_widget(self.bg_widget)

		self.bind(current_map=self.auto_switch_maps)
		self.bind(current_player_chapter=self.auto_load_maps)
		Window.bind(on_key_down=self.key_action)
		self.current_player_id = 0
		self.current_chapter = 0		
		self.current_map = 0
	def auto_load_maps(self, instance, current_player_chapter):
		print('[*]current_player_chapter:', current_player_chapter)
		p,c = current_player_chapter[0], current_player_chapter[1]
		self.map_path = f'res/chapters/{p}_{c}/maps/'	
		self.chapter_maps = []
		for f in os.listdir(self.map_path):
			if '.jpg' in f or '.png' in f:
				print(f'player_id:{p}, chapter_id:{c}, f:{f}')
				self.chapter_maps.append(os.path.join(self.map_path,f))
		self.current_map = -1
		self.current_map = 0
	def auto_switch_maps(self,instance, current_map):
		if current_map >= 0:
			print('[*]current map:', current_map)
			print("self.chapter_maps:",self.chapter_maps)
			print("self.chapter_maps[current_map]:",self.chapter_maps[current_map])
			bg = Rectangle(source=self.chapter_maps[current_map], pos=(0,0), size=(global_w,global_h),group='bg')
			self.bg_widget.load_bg(bg)

	def key_action(self, *args):
		press_key_id = args[1]
		press_key = args[3]
		if press_key_id in [276,275]:#<-,->
			self.exploring_maps(press_key_id)
		elif  press_key_id == 109:#m:
			self.current_chapter = turns[self.current_chapter]
		elif  press_key_id == 110:#n:
			self.current_player_id = turns[self.current_player_id]

	def exploring_maps(self, press_key_id):

			num = len(self.chapter_maps)
			if press_key_id==276:
				print ("key action left")
				if self.current_map <= 0:
					self.current_map = num - 1
				else:
					self.current_map -= 1				
			elif press_key_id==275:
				print ("key action right")
				if self.current_map >= num - 1:
					self.current_map = 0
				else:
					self.current_map += 1



class BG_widget(Widget):
	def __init__(self,**kwargs):#, bg_size, bg_pos, bg_source):
		super(BG_widget, self).__init__()
		print(f'init bg, self.parent:{self.parent}')		

	def load_bg(self,bg):
		self.parent.canvas.before.add(bg)

	def on_touch_down(self, touch): #For the flexibility to implement some user interaction functions on the whole screen
		#print('bg on_touch_down')
		print(touch)
		print(touch.pos,touch.spos)
		f = open('touch.txt','w')
		f.write('touch event:\n')
		print(touch.spos[0],touch.spos[1])
		f.write(f'touch spos:({touch.spos[0]},{touch.spos[1]})')
		f.close()

class NTUPLE_Story(App):
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ObjectScreen(name='object')) 
        sm.get_screen('object').start()
        sm.current = 'object'

        return sm

if __name__ == '__main__':
    if OS == "Windows":
        Window.fullscreen = 'auto'
    Config.set('kivy','keyboard_mode','')
    NTUPLE_Story().run()

