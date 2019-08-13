# -*- coding: utf-8 -*-
import pandas as pd
import json

path = 'res/h.[合成]表 - 工作表1.csv'
final_data_dict = {}

df = pd.read_csv(path)  
print(df)
print(df.keys())

for i, object_name in enumerate(df['輸出道具']):
	final_data_dict[object_name]['input1'] = df['合成輸入一'][i]
	final_data_dict[object_name]['input2'] = df['合成輸入二'][i]

