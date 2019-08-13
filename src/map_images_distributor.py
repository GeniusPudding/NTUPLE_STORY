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
print(os.getcwd())
abs_path = os.getcwd()
print(df)
print(df.keys()[1:])
for k in df.keys()[1:]:
	for name in df[k]:
		if not isinstance(name, float):
			map_name = name.split('\'')[1]
			print("map_name:",map_name)
			p,c = int(name[0])-1,int(name[2])-1
			map_dir = 'res/chapters/'+str(p)+'_'+str(c)+'/maps/'
			for im in os.listdir(map_dir):
				os.remove(os.path.join(map_dir, im))

			if len(map_name)==0:
				continue
			for im in imgs:
				if map_name in im:
					print('map_name found:',map_name)
					shutil.copy(os.path.join('res/images/handpainting/',im),map_dir)# os.path.join(map_dir,im))


		


