###################################################
# ePo screen for the game                    #
###################################################
from game_manager import *

class ePoScreen(Screen):
	cur_select_chapter_id = NumericProperty(-1)
	phonescreen_state = ListProperty([False,False])
	detailing = BooleanProperty(False)
	def __init__(self, player_id=0,chapter_id=0, **kwargs):
		super(ePoScreen, self).__init__(**kwargs)
		self.player_id = player_id
		self.chapter_id = chapter_id
		self.size = (self.screen_x,self.screen_y) = get_screen_size()
		print('ePoScreen.size:',self.size)

		self.phone_pos_hint = {'x':.35,'y':.025}
		self.phone_size_hint = (.3,.95)
		self.canvas.add(Color(.718, .831, .941, 1))
		self.canvas.add(Rectangle(pos=self.pos, size=self.size))
		self.phone = Image(source='res/images/phone/phone_messege.png',pos_hint=self.pos_hint , size_hint=self.size_hint,allow_stretch=True,keep_ratio=False )
		self.add_widget(self.phone)

		btn_len = min(.1*global_w, .2*global_h)
		# self.canvas.add(Color(0, 0, 0, .9))
		# self.canvas.add(Ellipse(pos=(.2*global_w, 0), size=(btn_len,btn_len)))
		# self.canvas.add(Color(1, 1, 1, .8))
		# self.canvas.add(Ellipse(pos=(.2*global_w+btn_len/10, btn_len/10), size=(.8*btn_len,.8*btn_len)))
		# self.add_widget(Label(text='Press\nEnter',color=(.2,.2,.2,1),font_size=40,pos=(.2*global_w+btn_len/10, btn_len/10), size=(.8*btn_len,.8*btn_len), size_hint=(None,None)))
		self.canvas.add(Color(0, 0, 0, .9))
		self.canvas.add(Ellipse(pos=(.05*global_w, 0), size=(btn_len,btn_len)))
		self.canvas.add(Color(1, 1, 1, .8))
		self.canvas.add(Ellipse(pos=(.05*global_w+btn_len/10, btn_len/10), size=(.8*btn_len,.8*btn_len)))
		self.add_widget(Label(text='Back!',color=(.2,.2,.2,1),font_size=40,pos=(.05*global_w+btn_len/10, btn_len/10), size=(.8*btn_len,.8*btn_len), size_hint=(None,None)))
		self.add_widget(Button(on_press=self.back_to_story,background_color=(1,1,1,0),pos_hint={'x':.05,'y':0},\
			size_hint=(btn_len/global_w,btn_len/global_h)))
		self.select_py = [.697,.609,.521,.433] 
		self.select_px = [.335,.665]
		self.detail_image = Image(source='res/images/phone/phone_messege.png',size_hint=(1,1),allow_stretch=True,keep_ratio=False)
		self.bind(cur_select_chapter_id=self.auto_select)
		Window.bind(on_key_down=self.key_action)

	def load_personal_ePo(self,player_id,chapter_id):
		self.player_id = player_id
		self.chapter_id = chapter_id
		self.phone.source = f'res/images/phone/{player_id}_{chapter_id}.jpg'
		self.cur_select_chapter_id = chapter_id - 1 

	def key_action(self,*args):
		if self.manager.current == 'epo':	
			press_key_id = args[1]
			if self.chapter_id == 0:
				return True
			if press_key_id == 273:
				if self.cur_select_chapter_id <= 0:
					self.cur_select_chapter_id = self.chapter_id - 1 
				else:
					self.cur_select_chapter_id -= 1 
			elif press_key_id == 274: 
				if self.cur_select_chapter_id >= self.chapter_id - 1:
					self.cur_select_chapter_id = 0
				else:
					self.cur_select_chapter_id += 1 

			elif press_key_id == 13:
				if self.detailing:
					self.hide_achievement()
				else:
					try:
						self.manager.get_screen('gm').players[self.player_id]\
							.unread_achievement.remove(self.cur_select_chapter_id)

					except:
						print('[*] Exception! Chapter not exists')
					self.display_achievement()

			return True

	def auto_select(self,instance,cur_select_chapter_id):
		if 0 <= cur_select_chapter_id :
			print('[*] auto_select cur_select_chapter_id:',cur_select_chapter_id)
			if self.detailing:
				self.hide_achievement()
				self.display_achievement()
			else:
				self.canvas.remove_group('select')
				self.canvas.add(Color(rgba=(0,182/255,1,.2),group='select'))
				self.canvas.add(Rectangle(pos=(.335*global_w,self.select_py[cur_select_chapter_id+1]*global_h),size=(.33*global_w,.088*global_h),group='select'))
		else:
			self.canvas.remove_group('select')
	def display_achievement(self):
		self.detailing = True
		self.detail_image.source = f'res/images/phone/{self.player_id}_{self.cur_select_chapter_id+1}_0.jpg' 
		self.add_widget(self.detail_image)

	def hide_achievement(self):
		self.detailing = False
		self.remove_widget(self.detail_image)

	def back_to_story(self,btn):
		self.cur_select_chapter_id = -2
		self.manager.current = 'story'
		self.manager.get_screen('story').unread_count = -1
		c = len(self.manager.get_screen('gm')\
			.players[self.player_id].unread_achievement)
		self.manager.get_screen('story').unread_count = c
		
#for testing
class NTUPhone(Image):#deprecated
	executing_function = StringProperty('messege')
	def __init__(self,screen, **kwargs):
		super(NTUPhone, self).__init__(**kwargs)
		self.messege = 'res/images/phone/phone_messege.png'
		self.screen = screen
	def execute(self,instance, function):
		if function == 'messege':
			self.executing_function = 'messege'
			self.source = self.messege
		elif function == 'story':
			self.executing_function = 'story'
			self.source = 'res/images/phone/phone_story.png'
		elif function == 'NTU':
			self.executing_function = 'NTU'
			self.source = 'res/images/phone/phone_NTU.png' 
		else:
			pass

	def to_direct_messege(self,person,*args):
		if self.messege == 'res/images/phone/phone_messege.png':
			self.source = self.messege = 'res/images/phone/direct_messege.png'
		elif self.messege == 'res/images/phone/direct_messege.png':
			self.source = self.messege = 'res/images/phone/phone_messege.png'



	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
			print('touch phone:',touch.pos,touch.spos)





