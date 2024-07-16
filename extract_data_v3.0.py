import pandas as pd
import json
import copy
import numpy as np
import os

def extract_google_sheet(url):
    # 设置df显示所有的行和列
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    # 编辑url为需要的格式
    url = url.replace('/edit?gid=', '/export?format=csv&gid=')
    # 根据链接，从google sheet读取数据
    df = pd.read_csv(url, header=3)
    # 处理数据
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    # 将空值置为0
    # df = df.fillna()
    df['No\n序号'] = df['No\n序号'].fillna(0)
    # 转换数据类型
    # df = df.astype({'前值': int, '预测值': int, '实际值': int, 'Nilai\n分数':int})
    # 删除 序号列数据非法的行
    df = df.drop(df[df['No\n序号'] == '备注：'].index)

    return df

def get_title_json(title_path):
    # 从标题文件中读取数据结构
    with open(title_path, 'r', encoding='utf-8') as f:
        data = f.read()
        json_data = json.loads(data)
        return json_data

def set_data_title(template, df):
    section_list = ['human_resource','finance','material','agriculture','industry',
      'commerce', 'big_data','internet','ai','legal']
    language_list = ['china', 'indonesia', 'double']

    data = copy.deepcopy(template)
    # 配置循环中需要的标识符
    index_df = 0  # df结构中的行
    index_section_list = -1 # 当前section在section_list中的位置，用来判断当前的section
    section_start_row = 0 # 当前section的起始行，用来判断sub行在section中的位置

    while index_df < len(df):
        # 获取index列的值，通过该列的值，判断当前行是sub小标题还是大标题
        index_value = int(df.iloc[index_df, 0])
        # 如果是大标题
        if index_value != 0:
            # 获取当前section的起始行
            section_start_row = index_df
            # 设置当前的section_list的index
            index_section_list += 1
            # 判断现在是哪个section
            section = section_list[index_section_list]
            index_df += 1
        elif index_value == 0:
            # # 判断现在是哪个section
            section = section_list[index_section_list]
            index_sub = index_df - section_start_row - 1
            for index_data in range(3,8):
                if index_data == 6:
                    continue
                data_temp = df.iloc[index_df,index_data+1]
                if pd.isnull(data_temp):
                    continue
                data_temp = str(data_temp).split('\n\n')
                if len(data_temp) == 2:
                    data['china'][section]['sub'][index_sub][index_data] = data_temp[1]
                    data['indonesia'][section]['sub'][index_sub][index_data] = data_temp[0]
                    data['double'][section]['sub'][index_sub][index_data] = data_temp[0] + '\n' + data_temp[1]
                elif len(data_temp) == 1:
                    for language in language_list:
                        data[language][section]['sub'][index_sub][index_data] = data_temp[0]

            data_temp = df.iloc[index_df, 7]
            if (~np.isnan(data_temp)) and len(str(data_temp).strip())>0:
                for language in language_list:        
                    data[language][section]['sub'][index_sub][6] = int(data_temp)
            index_df += 1
    return data

def data_to_json(data, output_file):
    # 将数据写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)

title_path = 'title_result.json'

url_data_sheet = {'week2': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=182614782#gid=182614782'}
output_file = 'data_result.json'

df = extract_google_sheet(url_data_sheet['week2'])
# print(df)
template = get_title_json(title_path)
data = set_data_title(template, df)
data_to_json(data, output_file)
