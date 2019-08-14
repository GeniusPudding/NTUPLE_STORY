# -*- coding: utf-8 -*-
###################################################
# Parse all .csv files for generating an all-     #
# 	object table before executing main.py  		  #
###################################################
import pandas as pd
import json
import sys 
import os
path = 'res/objects'


data_dict = {}
final_data_dict = {}
name_to_id = {}
if os.path.isfile('res/allocate_all_objects_table.json'):
	f = open('res/allocate_all_objects_table.json','r')
	data_dict = json.load(f)
	print('exist data:',data_dict)
	f.close()

object_count = 0
function_names = {'道具':'item','解碼':'puzzle','開鎖':'lock','合成':'synthesis','切換場景':'switching','觸發':'trigger','線索':'clue'}
chapter_code = {'一':0,'二':1,'三':2,'四':3}
player = {'A':0,'B':1,'C':2,'D':3}
#for testing
max_len_description = 0
m = 0
for f in os.listdir(path):#0.csv,1.csv,2.csv,3.csv
	if '.csv' in f:

		df = pd.read_csv(os.path.join(path,f))  
		print(df)
		print(df['物件一覽表'])

		for i,object_name in enumerate(df['物件一覽表']):#TODO:把df['取得章節']之格式規範清楚
			if isinstance(object_name,float):
				continue

			#try:
			if True:
				content = {'pos_hint':None,'size_hint':None,'source':None}#最後應該只有'nothing'的'source'是None


				if object_name in data_dict.keys():#only include{'pos_hint':pos_hint,'size_hint':size_hint,'source':source}
					print(f'{object_name} data exist!')
					print(data_dict[object_name])
					content = data_dict[object_name]
				else: 	
					print(f'{object_name} setting not exist!\nGo to the main screen to set the pos and size!\n')	
				
				print(f'init content:{content}')

				content['name'] = object_name

				content['on_map'] = True
				print(df['物件一覽表'][i])
				loc = df['所在地點'][i]#.split('\'')
				if len(loc.split('\'')) <= 1:
					print(f'特殊地點:{loc}，需另外配置')
					content['on_map'] = False
					content['map_name'] = None
				else:
					content['map_name'] = loc.split('\'')[1]  

				content['player'] = player[f[11]]

				content['chapter'] = [0,1,2,3]

				if not isinstance(df['取得章節'][i],float):    #len(df['取得章節'][i]) > 0:
					content['chapter'] = []
					for chap in df['取得章節'][i].split('、'):
						content['chapter'].append(chapter_code[chap])
				
				func = df['功能'][i]
				if len(func) <= 1:
					content['function_types'] = ['nothing']
				else:
					func = df['功能'][i].split('、')
					func_types = []
					for chinese in func:
						func_types.append(function_names[chinese])
					content['function_types'] = func_types

				if 'nothing' in content['function_types'] or 'clue' in content['function_types']:
					content['source'] = None	
				else:
					for img in os.listdir('res/images/handpainting/') :
						if ('.png' in img or '.jpg' in img) and object_name in img:
							content['source'] = os.path.join('res/images/handpainting/',img)

				if not isinstance(df['文字說明'][i], float):
					content['description'] = df['文字說明'][i]
					if len(content['description']) > max_len_description:
						max_len_description = len(content['description'])
				else:
					content['description'] = ''
				#'name','source','map_name','pos_hint','size_hint','player','chapter','function_types','description', on_map=True

				print(f'final content:{content}')

				final_data_dict[object_count] = content
				if object_name in name_to_id.keys():
					if not isinstance(name_to_id[object_name],list):
						name_to_id[object_name] = [name_to_id[object_name]]
					name_to_id[object_name].append(object_count)
					print('重覆!')
					m += 1
				else:
					name_to_id[object_name] = object_count 
				object_count += 1
			else:
			#except:
				print('Exception! object_name:',object_name)
				line = ''
				for k in df.keys():
					line += str(df[k][i]) 
					line += '__'
				line += '\n'
				print(line)
			#'player':self.current_player_id,'chapter':self.current_chapter,'map':self.current_map,	



print(f'final data_dict:{final_data_dict}')
print(f'final data_dict.keys():{final_data_dict.keys()}')
for i in range(135):
	if i not in final_data_dict.keys():
		print('i:',i)
print('m:',m)
print(f'final data_dict[118]:{final_data_dict[118]}')
print(f'final data_dict[125]:{final_data_dict[125]}')
print(f'final data_dict[127]:{final_data_dict[127]}')


c = 0
less = []
for content in final_data_dict.values():
	if content['source'] == None and 'item' in content['function_types'] :
		c += 1
		less.append(content['name'])
print('缺少圖片張數:',c)
print(less)
print()
print(os.listdir('res/images/handpainting/'))

print('max_len_description:',max_len_description)
with open('res/objects/final_objects_table.json','w') as f:
	json.dump(final_data_dict, f)	

print('name_to_id:',name_to_id)
print('name_to_id.values():',name_to_id.values())
print('len(name_to_id.values()):',len(name_to_id.values()))
with open('res/objects/name_to_id_table.json','w') as f:
	json.dump(name_to_id, f)	

