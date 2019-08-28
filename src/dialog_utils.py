###################################################
# Implement all common dialog tools here          #
# "Screen" must be an intance og kivy Screen      #
###################################################
from game_manager import *
special_char_time = .27
common_char_time = .115
next_line_time = .45

#TODO: 自動撥放一鍵加速功能
#Auto-dialog tools part:
def auto_play_dialog(Screen,auto_dialog, *args):#Main entry function, a Screen-bind function
	print('[*] Start auto play dialog')
	f = open('velocity.txt','r')
	r = f.read().split(',')
	print('auto r:',r)
	s_time = float(r[0])
	c_time = float(r[1])
	n_time = float(r[2])
	print('s_time,c_time,n_time:',s_time,c_time,n_time)

	start_line_clock_time = auto_dialog_preprocess(auto_dialog,s_time,c_time,n_time)#, auto_dialog 
	clock_time_accu = 0
	p = Screen.current_player_id
	c = Screen.current_chapter
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
					Clock.schedule_once(partial(Screen.bg_widget.load_bg,source),i*.5+clock_time_accu)
					switch_id += 1


			event = Clock.schedule_once(partial(line_display_scheduler,Screen,line,(i==len(auto_dialog)-1),s_time,n_time,c_time,name), .5+i*.5+clock_time_accu)#.5 is from the screen start
			Screen.dialog_events.append(event)		

			last_line = line.strip('\n')

	else:
		for i,(name,line) in enumerate(auto_dialog):#displaying
			clock_time_accu += start_line_clock_time[i]
			event = Clock.schedule_once(partial(line_display_scheduler,Screen,line,(i==len(auto_dialog)-1),s_time,n_time,c_time,name), .5+i*.5+clock_time_accu)#.5 is from the screen start
			Screen.dialog_events.append(event)

def auto_dialog_preprocess(auto_dialog,s_time,c_time,n_time):
	#preprocessing:
	#new_auto_dialog= dialog_segmentation(auto_dialog,20)#deprecated for displaying flexible length text line 

	start_line_clock_time = [0]#display time for each line
	for _,line in auto_dialog:#for i,(_,line) in enumerate(auto_dialog):
		time = cal_line_time_accu(line,s_time,c_time,n_time)#new_auto_dialog,line,i,start_line_clock_time)#start_line_clock_time = 
		print('\\n in line:',('\n' in line))
		start_line_clock_time.append(time)	
	#print('after preprocessing, new_auto_dialog:',new_auto_dialog,'start_line_clock_time:',start_line_clock_time)	
	return start_line_clock_time #,new_auto_dialog
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
				#print('add new_line:',new_line)
				new_dialog.append(new_line)
				new_line = [name,p]	
		new_line[1] += '\n'
		#print('add new_line:',new_line)	
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
	#print("custom_multisplit:",result_string)
	return result_string


def line_display_scheduler(Screen,line,last_autoline,ts,tn,tc,name='',close_dialogframe=False,uncontinuous=False,*args):#or chars_of_row = 15,rows = 3
	#TODO:auto close_dialogframe function after the chars displayed
	Screen.current_line = line 
	Screen.text_cleared = False
	Screen.current_speaker_name = name# #trigger auto_display_speaker
	print(f'Line display name:{Screen.current_speaker_name},line:{line}')
	
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

	clear_displayed_text(Screen,Screen.displaying_character_labels)
	if uncontinuous:
		for event in Screen.dialog_events:
			event.cancel()
	print('len(displaying_character_labels)=',len(Screen.displaying_character_labels))
	if len(Screen.displaying_character_labels) > 0:#testing
		print('有字幕殘留')
	
	print('start generate line:',line)
	Screen.displaying_character_labels = line_to_labels(line,chars_of_row,rows) #bijection to line characters 
	
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
		clear_displayed_text(Screen,displaying_character_labels)


def clear_displayed_text(Screen,displaying_character_labels,*args):#must between the last line characters displayed and the next line be processed  
	print('[*]clear_displayed_text!')
	for label in displaying_character_labels:
		Screen.remove_widget(label)
	Screen.displaying_character_labels = []
	#Screen.text_cleared = True
def line_to_labels(line,chars_of_row,rows):
	labels = []
	page_char_count = 0
	(tx,ty) = total_use = (.79,.17)
	(dx,dy) = char_distance = (.01,.01)
	(cx,cy) = char_size_hint = ((tx+dx)/chars_of_row - dx,(ty+dy)/rows - dy)#default (.07,.08)
	
	font_size = int(round(96/rows))

	#print('cx,cy:',cx,cy)
	#print('chars_of_row,rows:',chars_of_row,rows)
	for char in line:
		if char != '\n':
			col = page_char_count % chars_of_row#page_char_count % 10
			row = rows - 1 - page_char_count // chars_of_row#1 - page_char_count // 10
			#print(f'pos_hint:{.03+(cx+dx)*col}, {(cy+dy)*row}, col:{col}, row:{row}')
			labels.append(Label(text=char,pos_hint={'x':.03+(cx+dx)*col,'y':(cy+dy)*row},color=(1,1,1,1),font_size=font_size,size_hint=char_size_hint,font_name= 'res/HuaKangTiFan-CuTi-1.otf'))
			page_char_count += 1
		else:#won't be displayed
			labels.append(Label(text=char,pos_hint={'x':0,'y':0},color=(1,1,1,1),font_size=36,size_hint=char_size_hint,font_name= 'res/HuaKangTiFan-CuTi-1.otf'))
			page_char_count = 0
	return labels

#Manual-dialog tools part:
def semi_auto_play_dialog(Screen,dialog):#TODO: finish the plot mode functions
	print('[*] Start manual play dialog')	
	first_line_node = semi_auto_dialog_preprocess(dialog,'flexable')


	print('first_line_node.text_line:',first_line_node.text_line)
	line_display_scheduler(Screen,first_line_node.text_line,False,special_char_time,next_line_time,common_char_time,name=first_line_node.speaker)
	#screen_auto_display_node(first_line_node)
	return  first_line_node

class DialogListnode(object):
	def __init__(self,speaker,text_line,node_type):#,switch_map_path=None):
		self.speaker = speaker
		self.text_line = text_line
		self.type = node_type#"inner","head","tail"
		self.last = None
		self.next = None
		#self.switch_map = switch_map_path#需要支援返回對話時切換回上一張場景嗎
		#TODO: 在對話撥放的同時切換map
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
	# #testing
	# node = head_node

	# while node.get_next() is not None:
	# 	print(node.text_line)
	# 	node = node.get_next()
	return head_node
