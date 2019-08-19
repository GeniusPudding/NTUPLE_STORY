# -*- coding: utf-8 -*-
###################################################
# Parse all .csv files for generating an all-     #
# 	object table before executing main.py  		  #
###################################################
import pandas as pd
import json
import os
path = 'res/p. 探索模式npc表 - 工作表1.csv'

data_dict = [[{},{},{},{}],[{},{},{},{}],[{},{},{},{}],[{},{},{},{}]]


df = pd.read_csv(path)
print(df)
print(df.keys())

npc_id = 0
for i,npc_name in enumerate(df['人物']):
	if isinstance(df['章節'][i],float):
		continue
	p = int(df['章節'][i].split('_')[0]) - 1
	c = int(df['章節'][i].split('_')[1]) - 1
	data_dict[p][c][npc_id] = {'map_name':df['場景'][i],'npc_name':npc_name,'dialog':df['對話'][i],'get_item':None}
	if df['取得道具'][i] != 'X':
		data_dict[p][c][npc_id]['get_item'] = df['取得道具'][i]
	npc_id += 1
		
for p in range(4):
	for c in range(4):
		if len(data_dict[p][c]) > 0:
			npc_path = f'res/chapters/{p}_{c}/NPCs/'
			if os.path.isfile(os.path.join(npc_path,'npc_info.json')):
				os.remove(os.path.join(npc_path,'npc_info.json'))

			with open(os.path.join(npc_path,'npc_info.json'),'w') as f:
				json.dump(data_dict[p][c], f)				