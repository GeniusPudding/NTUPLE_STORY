# -*- coding: utf-8 -*-
###################################################
# Parse j[解碼]表 - 工作表1.csv for generating a    #
# 	puzzle table before executing main.py         #
###################################################
import pandas as pd
import json


path = 'res/j[解碼]表 - 工作表1.csv'
final_data_dict = {}

df = pd.read_csv(path)  
print(df)
print(df.keys())


for i, object_name in enumerate(df['解碼之物件']):

	num = int(df['輸入'][i])
	code = []
	for c in range(4):
		code.append(num%10)
		num //=10
	code.reverse()
	#print('code:',code)
	content = {'input':code}

	if isinstance(df['輸出道具'][i], float):
		content['output_item'] = None
	else:
		content['output_item'] = df['輸出道具'][i]

	if isinstance(df['解鎖新場景'][i], float):
		content['new_scene'] = None
	else:
		content['new_scene'] = df['解鎖新場景'][i]		

	if isinstance(df['是否觸發'][i], float):
		content['trigger'] = False
	else:
		content['trigger'] = True

	final_data_dict[object_name] = content

print('final_data_dict:',final_data_dict)
with open('res/objects/puzzle_table.json','w') as f:
	json.dump(final_data_dict, f)	

