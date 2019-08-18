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


# data_dict = {}
final_data_dict = {}
name_to_id = {}
# if os.path.isfile('res/allocate_all_objects_table.json'):
# 	f = open('res/allocate_all_objects_table.json','r')
# 	data_dict = json.load(f)
# 	print('exist data:',data_dict)
# 	f.close()

object_count = 0
function_names = {'道具':'item','解碼':'puzzle','開鎖':'lock','合成':'synthesis','切換場景':'switching','觸發':'trigger','線索':'clue'}#'線索':改成道具
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

			content = {'pos_hint':None,'size_hint':None,'source':None}#最後應該只有'nothing'的'source'是None
			lb = df['左下'][i]
			rt = df['右上'][i]
			if not (isinstance(lb, float) or isinstance(rt, float)):
				[px,py] = lb[lb.find('(')+1:lb.find(')')].split(',')
				[tx,ty] = rt[rt.find('(')+1:rt.find(')')].split(',')
				print(lb,rt,i,px,py,tx,ty)
				content['pos_hint'] = (float(px),float(py))
				content['size_hint'] = (float(tx)-float(px),float(ty)-float(py))

			content['name'] = object_name

			content['on_map_name'] = False#True
			loc = df['所在地點'][i]#.split('\'')
			if len(loc.split('\'')) > 1:
			# 	print(f'特殊地點:{loc}，需另外配置')
			# 	content['on_map'] = False
			# 	content['map_name'] = None
			# else:
				content['on_map_name'] = loc.split('\'')[1]  
			else:
				print('道具欄')

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

			# #testing
			# if 'clue' in content['function_types']:
			# 	 content['function_types'].remove('clue')
			# 	 content['function_types'].append('item')

			if set(['nothing','clue','switching']) & set(content['function_types']) == set():
				for img in os.listdir('res/images/handpainting/') :
					if ('.png' in img or '.jpg' in img) and object_name == img.split('.')[0]:
						content['source'] = os.path.join('res/images/handpainting/',img)
						break

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


print(f'final data_dict:{final_data_dict}')
print(f'final data_dict.keys():{final_data_dict.keys()}')
for i in range(135):
	if i not in final_data_dict.keys():
		print('i:',i)
	if 'puzzle' in  final_data_dict[i]['function_types']:
		print(final_data_dict[i])
print('m:',m)

# c = 0
# less = []
# for content in final_data_dict.values():
# 	if content['source'] == None and 'item' in content['function_types'] :
# 		c += 1
# 		less.append(content['name'])
# print('缺少圖片張數:',c)
# print(less)
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

