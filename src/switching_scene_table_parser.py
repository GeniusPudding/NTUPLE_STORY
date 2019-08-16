# -*- coding: utf-8 -*-
###################################################
# Distribute all objects content info to each     #
# 	chapters' directory before executing main.py  #
###################################################

import pandas as pd
import json
import sys 
import os
import shutil 

path = 'res/l.回憶劇情模式場景切換表 - 工作表1.csv'#等表格完成
map_dict = {}

df = pd.read_csv(path)
print(df)
print(df.keys())

scene_dicts = [[{},{},{},{}],[{},{},{},{}],[{},{},{},{}],[{},{},{},{}]]

for i,scene_name in enumerate(df['場景']):
	try:
		content = {'scene':scene_name,'line':df['對話'][i]}
		#print('content:',content)
		if isinstance(df['朦朧'][i],float):
			content['hazy'] = False
		else:
			content['hazy'] = True		

		p,c = int(df['玩家章節'][i][0])-1,int(df['玩家章節'][i][2])-1
		#print('i:',i)
		scene_dicts[p][c][i] = content
		#print('scene_dicts[p][c][i]:',scene_dicts[p][c][i])
	except:
		print('[*]Exception i,scene_name:',i,scene_name)
for p in range(4):
	for c in range(4):
		scene_dir = 'res/chapters/'+str(p)+'_'+str(c)+'/scenes/'
		if not os.path.isdir(scene_dir):
			os.mkdir(scene_dir)
		else:
			for f in os.listdir(scene_dir):
				os.remove(os.path.join(scene_dir, f))	


		d = scene_dicts[p][c]
		with open(scene_dir+'plot_scenes.json','w') as f:
			json.dump(d, f)	
		print(f'p:{p},c:{c},scene_dicts[{p}][{c}]:{d}')

		hp = 'res/images/handpainting/'
		for i in d.keys():
			for img in os.listdir(hp) :
				if ('.png' in img or '.jpg' in img):
					if d[i]['hazy']:
						if d[i]['scene'] in img.split('.')[0] and '朦朧' in img.split('.')[0]:
							shutil.copy(os.path.join(hp,img), scene_dir)
					else:	
						if d[i]['scene'] == img.split('.')[0]:
							shutil.copy(os.path.join(hp,img), scene_dir)

