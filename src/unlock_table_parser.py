# -*- coding: utf-8 -*-
import pandas as pd
import json
import sys 
import os
path = 'res/g.[開鎖]表 - 工作表1.csv'

final_data_dict = {}



df = pd.read_csv(path)  
print(df)
print(df.keys())

for i, object_name in enumerate(df['物件一覽表']):

	if isinstance(object_name,float):
		continue
		
		


print(f'final data_dict:{final_data_dict}')
with open('res/objects/final_unlock_table.json','w') as f:
	json.dump(final_data_dict, f)	
