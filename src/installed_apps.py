from game_manager import *
#global_w,global_h = get_screen_size()

class AppScreen(Image): #TODO:  新訊息跳出功能
	cur_view_id = NumericProperty(0)
	def __init__(self,title,dir_path, **kwargs):
		#AppScreen is also a UI state machine
		self.views = self.load_app_state_screens(dir_path)
		self.source = self.views[0]
		self.allow_stretch=True
		self.keep_ratio=False
		super(AppScreen, self).__init__(**kwargs)	

		#print(f"in AppScreen, pos = {self.pos},size = {self.size}")#list
		#print(f"in AppScreen, pos_hint,size_hint:", self.pos_hint,self.size_hint)#default: pos = [0, 0],size = [100, 100]
		#self.size = (global_w*self.size_hint[0],global_h*self.size_hint[1])
		#self.pos = (global_w*self.pos_hint['x'],global_h*self.pos_hint['y'])
		#print(f"in AppScreen, pos = {self.pos},size = {self.size}")#list
		self.title = title
		self.bind(cur_view_id=self.auto_switch_app_view)
		#self.canvas.add(Rectangle(pos=self.pos, size=self.size))#pos,size = phone's pos,size
		# self.default_label = Label(text = '需付費解鎖此應用程式功能',text_size = self.size,font_size = 84, pos_hint = self.pos_hint,size_hint=self.size_hint,font_name= 'res/HuaKangTiFan-CuTi-1.otf')
		# self.add_widget(self.default_label)#remove in child
		#self.cur_view_id = 0#self.source #used in pausing view to store the current state view, implemented in child classes
	def load_app_state_screens(self, dir_path):
		views = []
		files = os.listdir(dir_path)
		app_name = dir_path.split('/')[-1]
		for f in files:
			if app_name in f and ('.jpg' in f or '.png' in f):
				fulldir_path = os.path.join(dir_path,f)
				if os.path.isfile(fulldir_path):
					views.append(fulldir_path)

		return views
	def on_touch_down(self, touch):
		#print("app on_touch_down touch.pos,touch.spos: ",touch.pos,touch.spos)
		pass

	def auto_switch_app_view(self, instance, value):

		self.source = self.views[value]
		print('auto_switch_app_view: ',self.source)
#TODO: child class to implement each app's functions

class Line(AppScreen):
	def __init__(self,title,dir_path, **kwargs):
		super(Line, self).__init__(title,dir_path,**kwargs)	
	def on_touch_down(self, touch):
		super(Line, self).on_touch_down(touch)
		print('Line!')

class Facebook(AppScreen):
	def __init__(self,title,dir_path, **kwargs):
		super(Facebook, self).__init__(title,dir_path,**kwargs)	
		# self.canvas.add(Color(0,0,0,.5))
		# self.canvas.add(Rectangle(pos=(global_w*.55,global_h*.065),size=(global_w*.05,global_h*.04)))
	def on_touch_down(self, touch):
		super(Facebook, self).on_touch_down(touch)
		print('Facebook!')
		print('views:',self.views)
		pos_x,pos_y = touch.pos
		if global_h*.065 <= pos_y and pos_y <= global_h*.105:# in fb app's selection bar
			if global_w*.55 <= pos_x and pos_x <= global_w*.6:
				self.cur_view_id = 1 
			elif global_w*.6 < pos_x and pos_x <= global_w*.65:
				self.cur_view_id = 2

			elif global_w*.35 < pos_x and pos_x <= global_w*.4:
				self.cur_view_id = 0



#TODO: need default app image 				
installed_list = [AppScreen(dir_path= 'res/images/phone/default/',title ='Default',pos_hint={'x':.35,'y':.025} ,size_hint=(.3,.95))] * 24
installed_list[13] = Line(dir_path= 'res/images/phone/line/',title ='Line',pos_hint={'x':.35,'y':.025} ,size_hint=(.3,.95))
installed_list[15] = AppScreen(dir_path= 'res/images/phone/msg/',title ='Messenger',pos_hint={'x':.35,'y':.025} ,size_hint=(.3,.95))
installed_list[18] = Facebook(dir_path= 'res/images/phone/fb/',title ='Facebook',pos_hint={'x':.35,'y':.025} ,size_hint=(.3,.95))
installed_list[21] = AppScreen(dir_path= 'res/images/phone/ig/',title ='Instagram',pos_hint={'x':.35,'y':.025} ,size_hint=(.3,.95))
