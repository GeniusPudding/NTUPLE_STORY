# -*- coding: utf-8 -*-
###################################################
# Parse g.[開鎖]表 - 工作表1.csv for generating an#
# 	unlock table before executing main.py  		  #
###################################################
import pandas as pd
import json

path = 'res/g.[開鎖]表 - 工作表1.csv'
final_data_dict = {}

df = pd.read_csv(path)  
print(df)
print(df.keys())

for i, object_name in enumerate(df['開鎖之物件']):

	final_data_dict[object_name] = {}
	if isinstance(df['輸入道具'][i],float):
		final_data_dict[object_name]['input_item'] = None
	else:
		final_data_dict[object_name]['input_item'] = df['輸入道具'][i]

	if isinstance(df['輸出道具'][i],float):
		final_data_dict[object_name]['output_item'] = None
	else:
		if len(df['輸出道具'][i].split(',')) > 1:
			final_data_dict[object_name]['output_item'] = df['輸出道具'][i].split(',')
		else:
			final_data_dict[object_name]['output_item'] = df['輸出道具'][i]

	if isinstance(df['解鎖新場景'][i],float):
		final_data_dict[object_name]['new_scene'] = None
	else:
		final_data_dict[object_name]['new_scene'] = df['解鎖新場景'][i]

	if isinstance(df['是否觸發'][i],float):
		final_data_dict[object_name]['trigger'] = False
	else:
		final_data_dict[object_name]['trigger'] = True
		


print(f'final data_dict:{final_data_dict}')
with open('res/objects/unlock_table.json','w',encoding='utf-16') as f:
	json.dump(final_data_dict, f)	
