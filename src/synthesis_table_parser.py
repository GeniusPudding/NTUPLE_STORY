# -*- coding: utf-8 -*-
###################################################
# Parse h.[合成]表 - 工作表1.csv for generating a #
# 	synthesis table before executing main.py      #
###################################################
import pandas as pd
import json

path = 'res/h.[合成]表 - 工作表1.csv'
final_data_dict = {}

df = pd.read_csv(path)  
print(df)
print(df.keys())

for i, object_name in enumerate(df['輸出道具']):
	s1_name = df['合成輸入一'][i]
	s2_name = df['合成輸入二'][i]
	final_data_dict[s1_name] = {}
	final_data_dict[s1_name]['input'] = s2_name
	final_data_dict[s1_name]['output'] = object_name
	final_data_dict[s2_name] = {}
	final_data_dict[s2_name]['input'] = s1_name
	final_data_dict[s2_name]['output'] = object_name


print(f'final data_dict:{final_data_dict}')
with open('res/objects/synthesis_table.json','w') as f:
	json.dump(final_data_dict, f)	
