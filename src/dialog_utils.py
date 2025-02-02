###################################################
# Implement all common dialog tools here          #
# "screen" must be an intance og kivy screen      #
###################################################
from game_manager import *
from UI_utils import auto_prompt
special_char_time = .27
common_char_time = .115
next_line_time = .45
auto_s_time = .4
auto_c_time = .15
auto_n_time = 1.5
special_char_list = ['？','，','！','。','、']
#TODO: 自動撥放一鍵加速功能
#Auto-dialog tools part:
def read_velocity_config():
	f = open('velocity.txt','r')
	r = f.read().split(',')
	print('auto r:',r)
	s_time = float(r[0])
	c_time = float(r[1])
	n_time = float(r[2])
	return s_time,c_time,n_time

auto_s_time,auto_c_time,auto_n_time = read_velocity_config()	
def auto_play_dialog(screen,auto_dialog, *args):#Main entry function, a screen-bind function
	print('[*] Start auto play dialog')
	#if screen.display_pausing == 0:
	screen.display_pausing = 1
	s_time,c_time,n_time = auto_s_time,auto_c_time,auto_n_time#read_velocity_config()
	print('s_time,c_time,n_time:',s_time,c_time,n_time)

	start_line_clock_time = auto_dialog_preprocess(auto_dialog,s_time,c_time,n_time)#, auto_dialog 
	clock_time_accu = 0
	p = screen.current_player_id
	c = screen.current_chapter
	print('p,c:',p,c)



	if (p == 2 and c == 1) or (p == 1 and c == 2):
		with open(f'res/chapters/{p}_{c}/dialogs/switch_scenes.json','r') as f:
			table = json.load(f)
			print('table:',table)
		last_line = ''#for switching scene
		switch_id = 0
		for i,(name,line)  in enumerate(auto_dialog):#displaying
			clock_time_accu += start_line_clock_time[i]

			print('last_line:',last_line)
			if switch_id < len(table.keys()):
				if len(table[str(switch_id)]['line'].split(':')) > 1:
					table_line =  table[str(switch_id)]['line'].split(':')[1]
				else:
					table_line = table[str(switch_id)]['line']
				print(f'table_line:',table_line)	

				if last_line == table_line:
					source = table[str(switch_id)]['source']
					print('Switch bg to:',source)
					Clock.schedule_once(partial(screen.bg_widget.load_bg,source),i*.5+clock_time_accu)
					switch_id += 1


			event = Clock.schedule_once(partial(line_display_scheduler,screen,line,(i==len(auto_dialog)-1),s_time,n_time,c_time,name,auto_line_id=i), .5+i*.5+clock_time_accu)#.5 is from the screen start
			screen.dialog_events.append(event)		

			last_line = line.strip('\n')

	else:
		for i,(name,line) in enumerate(auto_dialog):#displaying
			clock_time_accu += start_line_clock_time[i]
			event = Clock.schedule_once(partial(line_display_scheduler,screen,line,(i==len(auto_dialog)-1),s_time,n_time,c_time,name,auto_line_id=i), .5+i*.5+clock_time_accu)#.5 is from the screen start
			screen.dialog_events.append(event)

def auto_dialog_preprocess(auto_dialog,s_time,c_time,n_time):
	#preprocessing:
	#new_auto_dialog= dialog_segmentation(auto_dialog,20)#deprecated for displaying flexible length text line 

	start_line_clock_time = [0]#display time for each line
	for _,line in auto_dialog:#for i,(_,line) in enumerate(auto_dialog):
		time = cal_line_time_accu(line,s_time,c_time,n_time)#new_auto_dialog,line,i,start_line_clock_time)#start_line_clock_time = 
		print('\\n in line:',('\n' in line))
		start_line_clock_time.append(time)	
	return start_line_clock_time
def dialog_segmentation(dialog,max_count):
	new_dialog = []
	for name,line in dialog:
		partitions = custom_multisplit(line,['？','，','！','。','、',')'])
		char_count = 0
		new_line = [name,'']
		for p in partitions:			
			if len(p) + len(new_line[1]) <= 20:
				new_line[1] += p
			else:
				new_line[1] += '\n'
				new_dialog.append(new_line)
				new_line = [name,p]	
		new_line[1] += '\n'	
		new_dialog.append(new_line)

	return new_dialog

def cal_line_time_accu(line,s_time,c_time,n_time):
	print('cal s_time,c_time,n_time:',s_time,c_time,n_time)
	time = 0
	for char in line:
		if char in ['？','，','！','。','、',')']:
			time += s_time#special_char_time
		elif char == '\n':
			time += n_time#next_line_time
		else:
			time += c_time#common_char_time
	time += n_time#for 	end of line
	print('cal time:',time)
	return time

def custom_multisplit(string,split_list):
	result_string = []
	head_id = 0
	for i,char in enumerate(string):
		if char in split_list:
			result_string.append(string[head_id:i+1])
			head_id = i+1
		elif i == len(string)-1:
			result_string.append(string[head_id:i+1])
	return result_string


def line_display_scheduler(screen,line,last_autoline,ts,tn,tc,name='',close_dialogframe=False,uncontinuous=False,auto_line_id = 0,*args):
	screen.current_line = line 
	screen.text_cleared = False
	screen.current_speaker_name = name# #trigger auto_display_speaker
	screen.auto_line_id = auto_line_id
	print(f'Line display name:{screen.current_speaker_name},line:{line}')
	
	pages = line.split('\n')
	max_displaying_length = 0
	for page in pages:
		if len(page) > max_displaying_length:
			max_displaying_length = len(page)
	if max_displaying_length <= 20:
		chars_of_row = 10
		rows = 2
	elif max_displaying_length <= 45:
		chars_of_row = 15
		rows = 3
	elif max_displaying_length <= 80:
		chars_of_row = 20
		rows = 4
	elif max_displaying_length <= 125:
		chars_of_row = 25
		rows = 5
	else:
		print('Text Line is too long!! Not supported')
		return

	clear_displayed_text(screen,screen.displaying_character_labels)
	if uncontinuous:
		cancel_events(screen)
		# for event in screen.dialog_events:
		# 	event.cancel()
	print('len(displaying_character_labels)=',len(screen.displaying_character_labels))
	if len(screen.displaying_character_labels) > 0:#testing
		print('有字幕殘留')
	
	print('start generate line:',line)
	screen.displaying_character_labels = line_to_labels(line,chars_of_row,rows) #bijection to line characters 

	if last_autoline:
		screen.finish_auto = True
#testing	
	return display_character_labels(screen,line,ts,tn,tc)
#testing
def display_character_labels(screen,line,ts,tn,tc,restart_id=0):

	accu_time = 0
	char_time = 0
	for i,char in enumerate(line):
		if char in special_char_list:
			char_time = ts#special_char_time
		elif char == '\n':
			char_time = tn#next_line_time
			accu_time += char_time
		else:
			char_time = tc
		event = Clock.schedule_once(partial(clock_display_characters,screen,screen.displaying_character_labels, char, i+restart_id), accu_time)
		screen.dialog_events.append(event)

		if char != '\n':
			accu_time += char_time


	return accu_time
def clock_display_characters(screen,displaying_character_labels, char, char_id,*args):
	if char != '\n':
		try:
			screen.add_widget(displaying_character_labels[char_id])
			screen.current_char_id = char_id
		except:
			print(f'[*] Exception: {char_id}-th displayed')
	else:
		clear_displayed_text(screen,displaying_character_labels)


def clear_displayed_text(screen,displaying_character_labels,*args):#must between the last line characters displayed and the next line be processed  
	print('[*]clear_displayed_text!')
	for label in displaying_character_labels:
		screen.remove_widget(label)
	screen.displaying_character_labels = []
	#screen.text_cleared = True
def line_to_labels(line,chars_of_row,rows):
	labels = []
	page_char_count = 0
	(tx,ty) = total_use = (.79,.17)
	(dx,dy) = char_distance = (.01,.01)
	(cx,cy) = char_size_hint = ((tx+dx)/chars_of_row - dx,(ty+dy)/rows - dy)#default (.07,.08)
	
	font_size = int(round(96/rows))

	for char in line:
		if char != '\n':
			col = page_char_count % chars_of_row#page_char_count % 10
			row = rows - 1 - page_char_count // chars_of_row#1 - page_char_count // 10
			labels.append(Label(text=char,pos_hint={'x':.03+(cx+dx)*col,'y':(cy+dy)*row},color=(1,1,1,1),font_size=font_size,size_hint=char_size_hint,font_name= 'res/HuaKangTiFan-CuTi-1.otf'))
			page_char_count += 1
		else:#won't be displayed
			labels.append(Label(text=char,pos_hint={'x':0,'y':0},color=(1,1,1,1),font_size=36,size_hint=char_size_hint,font_name= 'res/HuaKangTiFan-CuTi-1.otf'))
			page_char_count = 0
	return labels

def auto_accelerate(screen, prompt = False):
	if len(screen.current_line.strip('\n').split('\n')) > 1:
		print('對話太長，暫時不支援加速')#TODO
		return 
	cancel_events(screen)
	Clock.schedule_once(partial(pause,screen),.3) 
	while screen.current_char_id < len(screen.current_line) - 1:
		try:
			l = screen.displaying_character_labels[screen.current_char_id+1]
			screen.add_widget(l)
		except:
			print('[*] Exception: no more labels')
		screen.current_char_id += 1
	if prompt:
		auto_prompt(screen,'r',{'x':.2,'y':.3},instance=screen, prompt=True,pre_info='等不及了',post_info='趕快接受人生')

def auto_pause(screen, pre_info='讓我冷靜兩秒鐘...',post_info='再次面對人生',*args):
	print('Pause the auto dialog')
	cancel_events(screen)
	auto_prompt(screen,'r',{'x':.2,'y':.3},instance=screen, prompt=True,pre_info=pre_info,post_info=post_info)
	Clock.schedule_once(partial(pause,screen),1.2) 				

#TODO: debug
def auto_continue(screen):
	print('Restart the auto dialog')
	screen.remove_widget(screen.prompt_label)
	s = screen.current_line[screen.current_char_id+1:]
	#先跑完該句剩下的
	s_time,c_time,n_time = auto_s_time,auto_c_time,auto_n_time#read_velocity_config()
	res_time = display_character_labels(screen,s,s_time,n_time,c_time,restart_id=screen.current_char_id+1)
	#再重新開始播放動畫
	screen.auto_dialog = screen.auto_dialog[screen.auto_line_id+1:]
	Clock.schedule_once(partial(auto_play_dialog,screen,screen.auto_dialog),res_time)#-> screen.display_pausing = 1
						
def cancel_events(screen,*args):
	for event in screen.dialog_events:
		event.cancel()	

def pause(screen,*args):
	screen.display_pausing = 2

#Manual-dialog tools part:
def semi_auto_play_dialog(screen,dialog):
	print('[*] Start manual play dialog')
	screen.clear_text_on_screen()
	first_line_node = semi_auto_dialog_preprocess(dialog,'flexable')

	print('first_line_node.text_line:',first_line_node.text_line)
	line_display_scheduler(screen,first_line_node.text_line,False,special_char_time,next_line_time,common_char_time,name=first_line_node.speaker)
	return  first_line_node

class DialogListnode(object):
	def __init__(self,speaker,text_line,node_type):#,switch_map_path=None):
		self.speaker = speaker
		self.text_line = text_line
		self.type = node_type#"inner","head","tail"
		self.last = None
		self.next = None

	def set_last(self,listnode):
		self.last = listnode
	def set_next(self,listnode):
		self.next = listnode
	def get_last(self):
		return self.last
	def get_next(self):
		return self.next

def semi_auto_dialog_preprocess(dialog,format):
	new_auto_dialog = dialog
	if format == 'flexable':#Cancel the fixed-length partition here to support the scene-switching function
		last_node = head_node = DialogListnode(new_auto_dialog[0][0],new_auto_dialog[0][1],'head')
	elif format == 'fixed-length':
		new_auto_dialog = dialog_segmentation(dialog,20) 
		last_node = head_node = DialogListnode(new_auto_dialog[0][0],new_auto_dialog[0][1],'head')		
	else:
		print('The format is not supported by the dialog system!')
	for name,line in new_auto_dialog[1:-1]:
		node = DialogListnode(name,line,'inner')
		last_node.set_next(node)
		node.set_last(last_node)
		last_node = node
	node = DialogListnode(new_auto_dialog[-1][0],new_auto_dialog[-1][1],'tail')
	last_node.set_next(node)
	node.set_last(last_node)

	return head_node
