###################################################
# NTUPhone screen for the game                    #
###################################################
from game_manager import *

class NTUPhoneScreen(Screen):#TODO: set a restart phone button
	phonescreen_state = ListProperty([False,False])
	def __init__(self, player_id=0,chapter_id=0, **kwargs):
		super(NTUPhoneScreen, self).__init__(**kwargs)
		self.player_id = player_id
		self.chapter_id = chapter_id
		self.size = (self.screen_x,self.screen_y) = get_screen_size()
		print('NTUPhoneScreen.size:',self.size)
		self.phone_pos_hint = {'x':.35,'y':.025}#(.35*self.screen_x,.025*self.screen_y)
		self.phone_size_hint = (.3,.95)#(.3*self.screen_x,.95*self.screen_y) 
		# self.canvas.add(Color(.718, .831, .941, 1))
		# self.canvas.add(Rectangle(pos=self.pos, size=self.size,source='res/images/phone/phone.png' ))
		# self.canvas.add(Color(1, 1, 1, 1))
		# self.canvas.add(Rectangle(pos=(.35*self.size[0],.025*self.size[1]),\
		#  size=(.3*self.size[0],.95*self.size[1]),source='res/images/phone/phone.png'))
		self.phone = NTUPhone(screen= self,source='res/images/phone/phone_messege.png',pos_hint=self.phone_pos_hint , size_hint=self.phone_size_hint,allow_stretch=True,keep_ratio=False )
		self.add_widget(self.phone)

class NTUPhone(Image):
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





