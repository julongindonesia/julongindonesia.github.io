import pandas as pd
import json
import copy
import re
import math
import os
import extract_title_v4 as title
import extract_data_v4 as data_fun

def extract_google_sheet(path):
    
    # 根据链接，从google sheet读取数据
    df = pd.read_csv(path, header=3)
    df = df.loc[0:109]
    # 处理数据
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    # 将空值置为0
    df['No\n序号'] = df['No\n序号'].fillna(0)
    # 转换数据类型
    # df = df.astype({'前值': int, '预测值': int, '实际值': int, 'Nilai\n分数':int})
    # 删除最后一行备注
    df = df.drop(df[df['No\n序号'] == '备注：'].index)
    return df

if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__),'100.csv')
    df = extract_google_sheet(path)

    output_file = os.path.join(os.path.dirname(__file__),'data_result.json')

    title_path = os.path.join(os.path.dirname(__file__),'title_result.json')
    # print(df)
    template = data_fun.get_title_json(title_path)
    data = data_fun.set_data_title(template, df)
    data_fun.data_to_json(data, output_file)

   