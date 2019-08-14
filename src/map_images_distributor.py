# -*- coding: utf-8 -*-
###################################################
# Distribute all background images to each        #
# 	chapters' directory before executing main.py  #
###################################################

import pandas as pd
import json
import sys 
import os
import shutil 
path = 'res/f.探索模式場景圖表 - 工作表1.csv'
imgs = os.listdir('res/images/handpainting/')
print(imgs)
final_data_dict = {}
df = pd.read_csv(path)  

abs_path = os.getcwd()
print(abs_path)
print(df)
print(df.keys()[1:])

not_found = []
for k in df.keys()[1:]:
	for name in df[k]:
		if not isinstance(name, float):
			map_name = name.split('\'')[1].strip()
			print("map_name:",map_name)
			p,c = int(name[0])-1,int(name[2])-1
			map_dir = 'res/chapters/'+str(p)+'_'+str(c)+'/maps/'
			if not os.path.isdir(map_dir):
				os.mkdir(map_dir)
			for im in os.listdir(map_dir):
				os.remove(os.path.join(map_dir, im))

			if len(map_name)==0:
				continue

			found = 0
			for im in imgs:
				if map_name == im.split('.')[0]:
					print(f'player:{p},chapter:{c},im:{im},map_name:{map_name} found')

					#not support in Windows?
					#shutil.copy(os.path.join('res/images/handpainting/',im),os.path.join(map_dir,im))# os.path.join(map_dir,im))
					src = os.path.join('res\images\handpainting', im)
					dst = os.path.join(map_dir,im).replace('/','\\')
					print('src:',src)
					print('dst:',dst)
					os.system(f'copy {src} {dst}')
					found = 1
					
			if not found:
				not_found.append(map_name)
				print(f'map_name:{map_name} NOT found!')

print(imgs)
print()
print(not_found)


