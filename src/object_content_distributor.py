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

with open('res/objects/final_objects_table.json','r') as f:
	objects_table = json.load(f)
dicts = [[{},{},{},{}],[{},{},{},{}],[{},{},{},{}],[{},{},{},{}]]

for i in objects_table.keys():
	content = objects_table[i]
	p = content['player']
	for c in content['chapter']:
		dicts[p][c][i] = content

for p in range(4):
	for c in range(4):
		object_dir = 'res/chapters/'+str(p)+'_'+str(c)+'/objects/'
		if not os.path.isdir(object_dir):
			os.mkdir(object_dir)
		else:
			for f in os.listdir(object_dir):
				os.remove(os.path.join(object_dir, f))	

		with open(object_dir+'chapter_objects.json','w') as f:
			json.dump(dicts[p][c], f)	
		print(f'p:{p},c:{c},dicts[{p}][{c}]:{dicts[p][c]}')
		