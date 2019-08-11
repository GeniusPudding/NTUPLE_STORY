###################################################
# Implement all common dialog tools here          #
# "Screen" must be an intance og kivy Screen      #
###################################################
from game_manager import *

speaker_name = {'A':'李語蝶(室友)','B':'司馬熏(男友)','C':'孟亦寒(哥哥)','D':'亓官楓(故友)','X':'女主角','M':'媽媽','F':'爸爸','N':'','L':'L','P':'P'}
#TODO: 顯示玩家角色真名
special_char_time = .6
common_char_time = .25
next_line_time = 1.5
#Auto-dialog tools part:
def auto_play_dialog(Screen,auto_dialog, *args):#Main entry function, a Screen-bind function
	print('[*] Start auto play dialog')
	start_line_clock_time, auto_dialog = auto_dialog_preprocess(auto_dialog)
	clock_time_accu = 0
	for i,(name,line)  in enumerate(auto_dialog):#displaying
		clock_time_accu += start_line_clock_time[i]
		event = Clock.schedule_once(partial(line_display_scheduler,Screen,speaker_name[name],line,(i==len(auto_dialog)-1),special_char_time,next_line_time,common_char_time), .5+i*.5+clock_time_accu)#.5 is from the screen start
		Screen.dialog_events.append(event)
def auto_dialog_preprocess(auto_dialog):
	#preprocessing:
	new_auto_dialog= dialog_segmentation(auto_dialog,20)
	start_line_clock_time = [0]#display time for each line
	for _,line in new_auto_dialog:#for i,(_,line) in enumerate(auto_dialog):
		time = cal_line_time_accu(line)#new_auto_dialog,line,i,start_line_clock_time)#start_line_clock_time = 
		start_line_clock_time.append(time)	
	print('after preprocessing, new_auto_dialog:',new_auto_dialog,'start_line_clock_time:',start_line_clock_time)	
	return start_line_clock_time,new_auto_dialog#auto_dialog
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
				print('add new_line:',new_line)
				new_dialog.append(new_line)
				new_line = [name,p]	
		new_line[1] += '\n'
		print('add new_line:',new_line)	
		new_dialog.append(new_line)

	return new_dialog

def cal_line_time_accu(line):
	time = 0
	for char in line:
		if char in ['？','，','！','。','、',')']:
			time += special_char_time
		elif char == '\n':
			time += next_line_time
		else:
			time += common_char_time
	
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
	print("custom_multisplit:",result_string)
	return result_string


def line_display_scheduler(Screen,name,line,last_autoline,ts,tn,tc,*args):
	#print(f'Line display name:{name},line:{line}')
	
	Screen.current_speaker_name = name#speaker_name[name] #trigger auto_display_speaker
	print(f'Line display name:{Screen.current_speaker_name},line:{line}')
	Screen.displaying_character_labels = line_to_labels(line) #bijection to line characters 
	accu_time = 0
	char_time = 0
	for i,char in enumerate(line):
		if char in ['？','，','！','。','、']:
			char_time = ts#special_char_time
		elif char == '\n':
			char_time = tn#next_line_time
			accu_time += char_time
		else:
			char_time = tc
		event = Clock.schedule_once(partial(clock_display_characters,Screen,Screen.displaying_character_labels, char, i), accu_time)
		Screen.dialog_events.append(event)

		if char != '\n':
			accu_time += char_time

	if last_autoline:# line_id == len(auto_dialog) - 1:
		Screen.finish_auto = True
	return accu_time
def clock_display_characters(Screen,displaying_character_labels, char, char_id,*args):
	if char != '\n':
		Screen.add_widget(displaying_character_labels[char_id])
	else:
		clear_dialogframe_text(Screen,displaying_character_labels)

def clear_dialogframe_text(Screen,displaying_character_labels,*args):#must between the last line characters displayed and the next line be processed  
	for label in displaying_character_labels:
		Screen.remove_widget(label)

def line_to_labels(line):
	labels = []
	page_char_count = 0
	char_size_hint = (.07,.08)
	for char in line:
		if char != '\n':
			col = page_char_count % 10
			row = 1 - page_char_count // 10
			labels.append(Label(text=char,pos_hint={'x':.03+.08*col,'y':.015+.09*row},color=(1,1,1,1),font_size=48,size_hint=char_size_hint,font_name= 'res/HuaKangTiFan-CuTi-1.otf'))
			page_char_count += 1
		else:#won't be displayed
			labels.append(Label(text=char,pos_hint={'x':0,'y':0},color=(1,1,1,1),font_size=36,size_hint=char_size_hint,font_name= 'res/HuaKangTiFan-CuTi-1.otf'))
			page_char_count = 0
	return labels

#Manual-dialog tools part:
def semi_manual_play_dialog(Screen,dialog):#TODO: finish the plot mode functions
	print('[*] Start manual play dialog')	
	first_line_node = semi_manual_dialog_preprocess(dialog)
	line_display_scheduler(Screen,speaker_name[first_line_node.speaker],first_line_node.text_line,False,special_char_time,next_line_time,common_char_time)
	#screen_auto_display_node(first_line_node)
	return  first_line_node
#def screen_auto_display_node(Screen,node):
	#name = node.speaker
	#line = node.text_line
	#event = Clock.schedule_once(partial(line_display_scheduler,Screen,speaker_name[name],line,False,special_char_time,next_line_time,common_char_time), .5)
	#Screen.dialog_events.append(event)

class dialog_listnode(object):
	def __init__(self,speaker,text_line,node_type,cur_map):
		self.speaker = speaker
		self.text_line = text_line
		self.type = node_type#"inner","head","tail"
		self.last = None
		self.next = None
		self.switch_map = cur_map
	def set_last(self,listnode):
		self.last = listnode
	def set_next(self,listnode):
		self.next = listnode
	def get_last(self):
		return self.last
	def get_next(self):
		return self.next

def semi_manual_dialog_preprocess(dialog):
	new_auto_dialog = dialog_segmentation(dialog,20)

	last_node = head_node = dialog_listnode(new_auto_dialog[0][0],new_auto_dialog[0][1],'head')
	for name,line in new_auto_dialog[1:-1]:
		node = dialog_listnode(name,line,'inner')
		last_node.set_next(node)
		node.set_last(last_node)
		last_node = node
	node = dialog_listnode(new_auto_dialog[-1][0],new_auto_dialog[-1][1],'tail')
	last_node.set_next(node)
	node.set_last(last_node)
	#testing
	node = head_node
	while node.get_next() is not None:
		print(node.text_line)
		node = node.get_next()
	return head_node

def switching_scene_lines(plot_text):
	lines_to_scene = []#(the line,the scene path)
	return lines_to_scene