from game_manager import *
from installed_apps import *


# class AppIcon(ImageButton):#ImageButton
# 	def __init__(self,app_screen, **kwargs):
# 		super(AppIcon, self).__init__(**kwargs)	
# 		self.app_widget = app_screen #an instance of AppScreen
# 		# self.canvas.add(Color(0,0,0,1))
# 		# self.canvas.add(Rectangle(pos=self.pos, size=self.size))
# 	# def on_press(self):
# 	# 	print('AppIcon on press')
# 	# 	self.add_widget(self.app_widget)
# 	# def on_touch_down(self, touch):
# 	# 	print('AppIcon on touch down: ',touch.pos)


class AppPauseView(Image):#or use a Floatlayout?
	def __init__(self,app_icon, app_name, app_pause_view, **kwargs):
		#pos_hint={'x':.35,'y':.025+.95/6} ,size_hint= (.2,.95*.72),allow_stretch=True,keep_ratio=False
		super(AppPauseView, self).__init__(**kwargs)	
		icon_len = min(.02*global_w,.048*global_h)
		print("app_icon, app_name, app_pause_view:",app_icon, app_name, app_pause_view)
		self.tag_icon = Image(source=app_icon,pos_hint={'x':.37,'y':.025+.95*(5/6+.005)},size_hint=(icon_len/global_w,icon_len/global_h),allow_stretch=True,keep_ratio=False)
		self.title = Label(color=(1,1,1,1),text=app_name,font_size=26,pos_hint={'x':.40,'y':.025+.95*(5/6+.005)} ,size_hint= (.05,icon_len/global_h))
		self.pause_view = Image(source=app_pause_view,pos_hint={'x':.35,'y':.025+.95/6} ,size_hint= (.2,.95*.67),allow_stretch=True,keep_ratio=False)#Image()#Label()#Image()
		self.offset_x = 0
	def set_pause_view(self, parent_screen):
		self.tag_icon.pos_hint['x'] += self.offset_x 
		self.title.pos_hint['x'] += self.offset_x 
		self.pause_view.pos_hint['x'] += self.offset_x
		parent_screen.add_widget(self.tag_icon)
		parent_screen.add_widget(self.title)
		parent_screen.add_widget(self.pause_view)
	def clear_pause_view(self, parent_screen):
		self.tag_icon.pos_hint['x'] -= self.offset_x 
		self.title.pos_hint['x'] -= self.offset_x 
		self.pause_view.pos_hint['x'] -= self.offset_x
		parent_screen.remove_widget(self.tag_icon)
		parent_screen.remove_widget(self.title)
		parent_screen.remove_widget(self.pause_view)
	def set_offset_x(self, x_ratio): #TODO: read the offset of x pos
		self.offset_x = x_ratio - .35
 
		return self
	def on_touch_down(self,touch):#TODO: from pausing, choose the correct touched app to run
		print('pausing on_touch_down touch:', touch.pos,touch.spos)
		return False
class TaskStack(Widget):
	def __init__(self, **kwargs):
		super(TaskStack, self).__init__(**kwargs)
		self.opened_list = [] #add app id here
		self.opened_apps = {} #dict for key:id, value:app
		#self.current_view_id = len(self.opened_list)-1
		self.center_view_id = -1
	def test(self):
		print(f"while test, self.pos:{self.pos},self.size:{self.size},self.pos_hint:{self.pos_hint},self.size_hint:{self.size_hint},self.parent.pos:{self.parent.pos},self.parent.size:{self.parent.size},self.parent.pos_hint:{self.parent.pos_hint},self.parent.size_hint:{self.parent.size_hint},self.parent:{self.parent}")
		


	def push_task(self, app_id): #task status from closed to running
		print('app_id,parent:',app_id,self.parent)
		print(f'while push stack,  self.pos:{self.pos},self.size:{self.size},self.pos_hint:{self.pos_hint},self.size_hint:{self.size_hint},self.parent.pos:{self.parent.pos},self.parent.size:{self.parent.size},self.parent.pos_hint:{self.parent.pos_hint},self.parent.size_hint:{self.parent.size_hint},self.parent:{self.parent}')
		if app_id not in self.opened_list:
			print("This task hasn't been opened!")
			self.opened_list.append(app_id)
			app = self.build_app_pause_view(app_id)
			self.opened_apps[app_id] = app
		else:#remove and push to stack top
			print("This task has been opened!")
			self.opened_list.remove(app_id)
			self.opened_list.append(app_id)
		print(f"Now self.opened_list:{self.opened_list},self.opened_apps:{self.opened_apps}")
	def remove_task(self,app_id): #task status from paused to closed
		print(f"while remove_task, self.pos:{self.pos},self.size:{self.size},self.pos_hint:{self.pos_hint},self.size_hint:{self.size_hint},self.parent.pos:{self.parent.pos},self.parent.size:{self.parent.size},self.parent.pos_hint:{self.parent.pos_hint},self.parent.size_hint:{self.parent.size_hint},self.parent:{self.parent} self.opened_list:{self.opened_list},self.opened_apps:{self.opened_apps}")
		if len(self.opened_list) == 1:
			self.parent.phonescreen_state[0] = False
			self.parent.phonescreen_state[1] = False
		else:
			app = self.opened_apps[app_id]
			#self.parent.remove_widget(app)
			app.clear_pause_view(parent_screen=self.parent) 
		self.opened_list.remove(app_id)
		del self.opened_apps[app_id]

		

	def build_app_pause_view(self,app_id):
		print(f"while building, self.pos:{self.pos},self.size:{self.size},self.pos_hint:{self.pos_hint},self.size_hint:{self.size_hint},self.parent.pos:{self.parent.pos},self.parent.size:{self.parent.size},self.parent.pos_hint:{self.parent.pos_hint},self.parent.size_hint:{self.parent.size_hint},self.parent:{self.parent},self.opened_list:{self.opened_list},self.opened_apps:{self.opened_apps}")
		
		app_list = installed_list
		app = app_list[app_id]
		app_name = app.title
		s = app.source
		print('s:',s)
		app_icon = s[:17] + 'icon/' + s[17:].split('/')[-2] + '.png'
		app_pause_view = app.views[app.cur_view_id] 
		print(f"app_name:{app_name},app_icon:{app_icon},app_pause_view:{app_pause_view}")
		view = AppPauseView(app_icon=app_icon, app_name=app_name, app_pause_view=app_pause_view,source=app_pause_view,pos_hint={'x':.35,'y':.025+.95/6} ,size_hint= (.2,.95*.72),allow_stretch=True,keep_ratio=False)#
		return view

	def display_pausing_list(self,gesture_type):#gesture_type 1:from desktop to pause view,gesture_type 0:from running to pause view
		#used when switch from other phonestate to pausing state, the entry of the pausing state 
		if gesture_type==1 and len(self.opened_list)==0:
			return #don't change phone state
		self.parent.phone.source = 'res/images/phone/phone_pause.jpg'

		self.parent.phonescreen_state = [False,True] 
		if gesture_type==0:
			self.parent.app_pause(Button())


		#self.parent.phonescreen_state[0] = False
		#self.parent.phonescreen_state[1] = True
		print("display_pausing_list gesture_type:",gesture_type)	
		print(f"while displaying, self.parent:{self.parent},self.opened_list:{self.opened_list},self.opened_apps:{self.opened_apps}")
		#main UI display part:
		for app_id in self.opened_list[:-3+gesture_type]:#the last three's pos maybe different 
			app = self.opened_apps[app_id]
			#app.pos_hint = {'x':.5,'y':.025+.95/6} 
			#app.size_hint = (.2,.95*.72)
			#self.parent.add_widget(app)
			app.set_pause_view(parent_screen=self.parent) #these apps pause view may be fully overlapped
			#self.parent.test_add_widget(app)
			print(f'apps:{app}')	


		if gesture_type == 0:
			if len(self.opened_list)>=3:
				app = self.opened_apps[self.opened_list[-3]].set_offset_x(.363)	
				print(f'app-3:{app},self.opened_apps:{self.opened_apps},self.opened_list:{self.opened_list}')	
				#self.parent.add_widget(app)
				app.set_pause_view(parent_screen=self.parent)
			if len(self.opened_list)>=2:
				app = self.opened_apps[self.opened_list[-2]].set_offset_x(.416)
				print(f'app-2:{app},self.opened_apps:{self.opened_apps},self.opened_list:{self.opened_list}')				
				#self.parent.add_widget(app)
				app.set_pause_view(parent_screen=self.parent)

				app = self.opened_apps[self.opened_list[-1]].set_offset_x(.575)		
				print(f'app-1:{app},self.opened_apps:{self.opened_apps},self.opened_list:{self.opened_list}')		
				#self.parent.add_widget(app)
				app.set_pause_view(parent_screen=self.parent)		
				self.parent.canvas.after.add(Color(.718, .831, .941, 1))#(1,1,1,1))#
				self.parent.canvas.after.add(Rectangle(pos=(.65*global_w,0),size=(.35*global_w,global_h)))#(.125,.95*.72*global_h)))
			if len(self.opened_list)==1:
				app = self.opened_apps[self.opened_list[-1]].set_offset_x(.4)		
				print(f'app-1:{app},self.opened_apps:{self.opened_apps},self.opened_list:{self.opened_list}')		
				#self.parent.add_widget(app)
				app.set_pause_view(parent_screen=self.parent)		

		elif gesture_type == 1:
			if len(self.opened_list)>=2:
				app = self.opened_apps[self.opened_list[-2]].set_offset_x(.355)		
				#self.parent.add_widget(app)
				app.set_pause_view(parent_screen=self.parent)	
			if len(self.opened_list)>=1:	
				app = self.opened_apps[self.opened_list[-1]].set_offset_x(.4)		
				#self.parent.add_widget(app)
				app.set_pause_view(parent_screen=self.parent)									
		#TODO: set the ipone pause view  

	def hide_pausing_list(self):
		#used when switch from pausing state to other phonestate
		print("when hiding, self.opened_list:",self.opened_list)
		for app_id in self.opened_list:
			app = self.opened_apps[app_id]
			#self.parent.remove_widget(app)
			app.clear_pause_view(parent_screen=self.parent) 

		self.parent.phone.source = 'res/images/phone/phone.jpg'	

class IPhoneXR(Image):#emulate Ipone XR gestures
	def __init__(self, **kwargs):
		super(IPhoneXR, self).__init__(**kwargs)
		self.start_touch_pos = (0,0)
		self.end_touch_pos = (0,0)
		self.start_touch_pos_hint = (0,0)
		self.end_touch_pos_hint = (0,0)

		print(f"in phone, pos_hint:{self.pos_hint},size_hint:{self.size_hint}")
	#TODO:實做所有的觸控功能在此類別:
	def on_touch_down(self, touch):
		print("phone on_touch_down touch.pos,touch.spos: ",touch.pos,touch.spos)
		#print("phone's parent:",self.parent)
		self.start_touch_pos = touch.pos
		self.start_touch_pos_hint = touch.spos
		#print(f"while on_touch_down, self.pos:{self.pos},self.size:{self.size},self.pos_hint:{self.pos_hint},self.size_hint:{self.size_hint},self.parent.pos:{self.parent.pos},self.parent.size:{self.parent.size},self.parent.pos_hint:{self.parent.pos_hint},self.parent.size_hint:{self.parent.size_hint},self.parent:{self.parent}")


		#app.pos_hint = {'x':.35,'y':.025+.95/6} 
		#app.size_hint = (.2,.95*.72)


	def on_touch_move(self, touch):
		#print("phone on_touch_move touch.pos,touch.spos: ",touch.pos,touch.spos)
		pass#TODO:gesture
	def on_touch_up(self, touch):
		print("phone on_touch_up touch.pos,touch.spos:",touch.pos,touch.spos)
		self.end_touch_pos = touch.pos
		self.end_touch_pos_hint = touch.spos
		#phonescreen_state[0]:running, phonescreen_state[1]:pausing
		#TODO: simulate the ipone XR's gesture
		#app.pos_hint = {'x':.35,'y':.025+.95/6} 
		#app.size_hint = (.2,.95*.72) (pausing view)
		#phone: pos_hint={'x':.35,'y':.025} ,size_hint=(.3,.95)
		
		#TODO: Exception handle before release
		#try:


		#For gestures 1, 2		
		if abs(self.start_touch_pos_hint[1]-(self.pos_hint['y']+0.025*self.size_hint[1]))< 0.025*self.size_hint[1]: 
			if self.end_touch_pos_hint[1]-self.start_touch_pos_hint[1]>0.15:	#gesture type 1: back to desktop
				print("testing gesture 1:",self.parent.phonescreen_state)
				if self.parent.phonescreen_state[0]: #from running
					self.parent.app_pause_and_back_to_desktop(Button())
				elif self.parent.phonescreen_state[1]: #from pausing
					self.parent.pause_view_back_to_desktop()
				else: #an exception of this gesture, from desktop 
					self.parent.tasks_stack.display_pausing_list(gesture_type=1)
			elif self.end_touch_pos_hint[1]-self.start_touch_pos_hint[1]>0.05: #gesture type 2:  display task_stack, <= 0.15
				print("testing gesture 2:",self.parent.phonescreen_state)
				if self.parent.phonescreen_state[0] : #from running
					self.parent.tasks_stack.display_pausing_list(gesture_type=0)
				elif not self.parent.phonescreen_state[1]: #from desktop
					self.parent.tasks_stack.display_pausing_list(gesture_type=1)
			
		#For pausing state to run app:
		if self.parent.phonescreen_state[1]:
			print("in pausing state gesture:",self.parent.tasks_stack.opened_list,self.parent.tasks_stack.center_view_id)
			if E2_distance(self.end_touch_pos,self.start_touch_pos) <= 0.01*min(global_w,global_h):#consider as no touch move
				if .183 < self.end_touch_pos_hint[1] and self.end_touch_pos_hint[1] < .903 :#end and start touch pos y in pausing view range 				
					self.parent.pause_to_run(self.parent.tasks_stack.opened_list[self.parent.tasks_stack.center_view_id])
				else:
					self.parent.pause_view_back_to_desktop()			
			else: #touch move, #gesture type 3: remove pausing app
				if .183 < self.start_touch_pos_hint[1] and self.start_touch_pos_hint[1] < .903  and (self.end_touch_pos_hint[1]-self.start_touch_pos_hint[1]) > max(.05,(self.end_touch_pos_hint[0]-self.start_touch_pos_hint[0])*2):
					print("remove")
					self.parent.tasks_stack.remove_task(self.parent.tasks_stack.opened_list[self.parent.tasks_stack.center_view_id])
					#TODO: Animation of remove app pause view to up

			#TODO:
			#gesture type 4:  Move left or right to choosing in task pause views 

			#gesture type 5:  Move left or right to choosing when running apps


		# except:
		# 	print("Exception gesture!")
		# 	print("self.parent.phonescreen_state[0]:",self.parent.phonescreen_state[0])
		# 	if self.parent.phonescreen_state[0]:
		# 		self.parent.app_pause_and_back_to_desktop(Button())	
def E2_distance(pos1,pos2):
	return math.sqrt(math.pow(pos1[0]-pos2[0],2)+math.pow(pos1[1]-pos2[1],2))	

class PhoneScreen(Screen):#TODO: set a restart phone button
	phonescreen_state = ListProperty([False,False])
	def __init__(self, owner_id=0, **kwargs):
		super(PhoneScreen, self).__init__(**kwargs)
		self.owner = owner_id
		self.size = (self.screen_x,self.screen_y) = get_screen_size()
		self.phone_pos_hint = {'x':.35,'y':.025}#(.35*self.screen_x,.025*self.screen_y)
		self.phone_size_hint = (.3,.95)#(.3*self.screen_x,.95*self.screen_y) 
		self.canvas.add(Color(.718, .831, .941, 1))
		self.canvas.add(Rectangle(pos=self.pos, size=self.size ))
		self.phone = IPhoneXR(source='res/images/phone/phone.jpg',pos_hint=self.phone_pos_hint , size_hint=self.phone_size_hint,allow_stretch=True,keep_ratio=False )
		self.add_widget(self.phone)
		self.tasks_stack = TaskStack()
		self.add_widget(self.tasks_stack)
		self.tasks_stack.test()
		print(f"init PhoneScreen, self.pos:{self.pos},self.size:{self.size},self.pos_hint:{self.pos_hint},self.size_hint:{self.size_hint},self.screen_x:{self.screen_x},self.screen_y:{self.screen_y}")
		#self.canvas.add(Color(1, 1, 1, .9))#source='res/images/phone/phone.jpg',
		#print("phone:",self.phone_pos,self.phone_size)
		#self.canvas.add(Rectangle(pos=self.phone_pos, size= self.phone_size)) 
		
		self.add_widget(ImageButton(callback=self.back_to_story,source='res/images/testing/back.png',pos= (self.screen_x*.1,self.screen_y*.05),size_hint=(None,None), size= (self.screen_x*.2,self.screen_y*.15)))
		#print(f'check1: self.pos:{self.pos},self.size:{self.size},self.pos_hint:{self.pos_hint},self.size_hint:{self.size_hint},self.screen_x:{self.screen_x},self.screen_y:{self.screen_y}')
	
		self.installed_app_id = [1,13,15,18,21]
		self.appscreens = installed_list #add child classes of AppScreen here 
		self.app_centers = [(0.422, 0.854), (0.474, 0.854), (0.526, 0.854), (0.578, 0.854), (0.422, 0.734), (0.474, 0.734), (0.526, 0.734), (0.578, 0.734), (0.422, 0.614), (0.474, 0.614), (0.526, 0.614), (0.578, 0.614), (0.422, 0.494), (0.474, 0.494), (0.526, 0.494), (0.578, 0.494), (0.422, 0.374), (0.474, 0.374), (0.526, 0.374), (0.578, 0.374), (0.422, 0.0945), (0.474, 0.0945), (0.526, 0.0945), (0.578, 0.0945)]

		row_center = [0.854, 0.734, 0.614, 0.494, 0.374, 0.0945]
		col_center = [0.422, 0.474, 0.526, 0.578]
		icon_size_hint = (.037,.0693)
		rad_x_hint = .0185
		rad_y_hint =.03465
		
		#Three state of the phone screen: running(True,False), pausing(False,True), desktop(False,False)
		#self.running = False
		#self.pausing = False #these two can't be True simultaneously
		self.phonescreen_state = [False,False]#means (self.running,self.pausing)
		self.lastscreen_state = [False,False]
		#print(f'check2: self.pos:{self.pos},self.size:{self.size},self.pos_hint:{self.pos_hint},self.size_hint:{self.size_hint},self.screen_x:{self.screen_x},self.screen_y:{self.screen_y}')

		#TODO: 將各個狀態所有須修改的屬性包裝好以及接口統一
		self.bind(phonescreen_state=self.phonescreen_state_monitor)
		#self.bind(size=self.checking)
		self.cur_running_app_id = -1
		self.desktop_icons = []
		for i,y in enumerate(row_center):
			for j,x in enumerate(col_center):#background_color=(1,1,1,.5),
				#print('x,y:',x,y)
				self.desktop_icons.append(Button(background_color=(1,1,1,0),on_press=self.app_run,pos_hint={'x':x-rad_x_hint,'y':y-rad_y_hint} ,size_hint= (.037,.0693)))#pos_hint={'x':x-rad_x_hint, 'y':y-rad_y_hint},size_hint=icon_size_hint))
		#print(f'check3: self.pos:{self.pos},self.size:{self.size},self.pos_hint:{self.pos_hint},self.size_hint:{self.size_hint},self.screen_x:{self.screen_x},self.screen_y:{self.screen_y}')

		self.set_icon_button()
	# def test_add_widget(self,app):
	# 	print('test_add_widget app.pos,app.size,app.pos_hint ,app.size_hint:',app.pos,app.size,app.pos_hint ,app.size_hint)
	# 	app.size_hint = [0.3, 0.6839999999999999]
	# 	print('test_add_widget app.pos,app.size,app.pos_hint ,app.size_hint:',app.pos,app.size,app.pos_hint ,app.size_hint)
	# 	self.add_widget(app)

	# def checking(self,instance, value):
	# 	print(f'in checking, instance:{instance}, value:{value},self.pos:{self.pos},self.size:{self.size},self.pos_hint:{self.pos_hint},self.size_hint:{self.size_hint},self.screen_x:{self.screen_x},self.screen_y:{self.screen_y}')

	def phonescreen_state_monitor(self,instance, value):
		#clear the widgets that should be in last state, and run the common step to get into the new state
		print(f'in phonescreen_state_monitor, self.lastscreen_state:{self.lastscreen_state}')
		if value == self.lastscreen_state:
			return
		if value == [False,False]:
			print(f"[*]into phonescreen state: {self.phonescreen_state}(desktop) ")
			#Clear part:
			if self.lastscreen_state == [True,False]:#from running get into desktop state
				self.remove_widget(self.appscreens[self.cur_running_app_id])
			elif self.lastscreen_state == [False,True]:#from pausing get into desktop state
				self.tasks_stack.hide_pausing_list()
			#Common part:
			self.cur_running_app_id = -1
			self.set_icon_button()
			self.lastscreen_state = [False,False]
		elif value[0] and not value[1]:
			print(f"[*]into phonescreen state: {self.phonescreen_state}(running) ")
			#Clear part:
			#print("in running state1, self.cur_running_app_id:",self.cur_running_app_id)
			if self.lastscreen_state == [False,False]:#from desktop get into running state
				self.tasks_stack.push_task(self.cur_running_app_id)
				self.clear_icon_button()
			elif self.lastscreen_state == [False,True]:#from pausing get into running state
				self.tasks_stack.hide_pausing_list()
			#print("in running state2, self.cur_running_app_id:",self.cur_running_app_id)	
			#Common part:
			self.add_widget(self.appscreens[self.cur_running_app_id])
			self.lastscreen_state = [True,False]

		elif value[1] and not value[0]:
			print(f"[*]into phonescreen state: {self.phonescreen_state}(pausing) ") #TODO: 讓桌面模糊化
			
			#Common part:
			if self.lastscreen_state == [False,False]:#from desktop get into pausing state
				self.clear_icon_button()
			elif self.lastscreen_state == [True,False]:#from running get into pausing state
				self.remove_widget(self.appscreens[self.cur_running_app_id])
			#Common part: #always call display_pausing_list
			self.lastscreen_state = [False,True]
		else:
			print(f"[*]into phonescreen state: {self.phonescreen_state}(ERROR!!) ")

	def set_icon_button(self):
		#when cur_running_app_id == -1, call this

		#if self.cur_running_app_id == -1:
		for btn in self.desktop_icons:
			# if btn.parent == self:
			# 	print(f'btn:{btn} has already added')
			# else:	
			self.add_widget(btn)
		#print('self.desktop_icons:',self.desktop_icons)

	def clear_icon_button(self):
		#when cur_running_app_id >= 0, call this
		#if self.cur_running_app_id >= 0:
		for btn in self.desktop_icons:
			self.remove_widget(btn)

	def app_run(self, btn):#the entry of the running state
		print('phone function: app_run')	

		self.phone.start_touch_pos = btn.last_touch.pos
		self.phone.start_touch_pos_hint = btn.last_touch.spos
		nearest_id = self.get_touched_nearest_id(btn)
		print("run app id: ",nearest_id)
		self.cur_running_app_id = nearest_id
		self.phonescreen_state[0] = True
		#for testing
		#self.add_widget(Button(text= "back to desktop",background_color=(.5,.5,.5,.5),on_press=self.app_puase_to_desktop,pos_hint={'x':.2,'y':.3},size_hint=(.1,.1)))
	def pause_to_run(self,app_id):#TODO:rewrite this to consider the opening order and the touch pos
		print('phone function: pause_to_run')	
		self.cur_running_app_id = app_id
		self.phonescreen_state[0] = True
		self.phonescreen_state[1] = False	
		

	def app_pause(self, btn):
		print('phone function: app_pause')	
		print('pause self.cur_running_app_id:',self.cur_running_app_id)
		self.cur_running_app_id = -1	

	def app_pause_and_back_to_desktop(self, btn):
		print('phone function: app_pause_and_back_to_desktop')	
		self.phonescreen_state[0] = False	
		self.phonescreen_state[1] = False		
		#self.remove_widget(self.appscreens[self.cur_running_app_id])
		
	def pause_view_back_to_desktop(self):
		print('phone function: pause_view_back_to_desktop')	
		self.phonescreen_state[0] = False
		self.phonescreen_state[1] = False
		#self.tasks_stack.hide_pausing_list()

	def load_personal_contacts(self):#switch to IG, messenger ,or line screen? 
		print(self.owner)
		


	def back_to_story(self,btn):
		print('back_to_story')
		self.phonescreen_state[0] = False
		self.phonescreen_state[1] = False
		if __name__ != '__main__':
			self.manager.current = 'story'

	def get_touched_nearest_id(self,btn):
		print('btn.last_touch.spos :',btn.last_touch.pos )
		touch_pos = btn.last_touch.pos
		nearest_id = -1 
		min_dis = 10000
		for i,c_pos_hint in enumerate(self.app_centers):
			cal = E2_distance(touch_pos,(c_pos_hint[0]*global_w,c_pos_hint[1]*global_h)) #math.sqrt(math.pow(touch_pos[0]-c_pos_hint[0]*global_w,2)+math.pow(touch_pos[1]-c_pos_hint[1]*global_h,2))
			#print(f"i:{i},cal:{cal},touch_pos:{touch_pos}")
			if  cal < min_dis:
				min_dis = cal 
				nearest_id = i
		
		return nearest_id

class TestPhoneApp(App):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.root = PhoneScreen(owner_id=1)
	def build(self):              
		return self.root
if __name__ == '__main__':
	TestPhoneApp().run()
