import pandas as pd
import json

# 设置df显示所有的行和列
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def get_data_google_sheet(url):
    # url_julong = url_julong.replace('/edit?gid=', '/export?format=csv&gid=')
    # worksheet = 'Copy of 100指数'
    # 根据链接，从google sheet读取数据
    df = pd.read_csv(url, header=3)
    # 处理数据
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    # 将空值置为0
    df = df.fillna(0)
    # 转换数据类型
    # df = df.astype({'前值': int, '预测值': int, '实际值': int, 'Nilai\n分数':int})
    return df

def get_data_json(path):
    # 从score.json中读取数据结构
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        json_data = json.loads(data)
        return json_data

def set_data(section, data, config, df):
    # 数据在df中的位置， 在json中的位置为 col-1
    pev_col = 4
    pred_col = 5
    real_col = 6
    score_col = 7
    start_row = config[section]['start_row']
    for i in range(0, 10):
        data[section][i][3] = int(df.iloc[start_row + i, pev_col])
        data[section][i][4] = int(df.iloc[start_row + i, pred_col])
        data[section][i][5] = int(df.iloc[start_row + i, real_col])
        data[section][i][6] = int(df.iloc[start_row + i, score_col])
    return data

my_config = {
    "human_resource": {
        "start_row": 1
    },
    "finance": {
        "start_row": 12
    },
    "material": {
        "start_row": 23
    },
    "agriculture": {
        "start_row": 34
    },
    "industry": {
        "start_row": 45
    },
    "commerce": {
        "start_row": 56
    },
    "big_data": {
        "start_row": 67
    },
    "internet": {
        "start_row": 78
    },
    "ai": {
        "start_row": 89
    },
    "legal":  {
        "start_row": 100
    }
}

url_julong = f'https://docs.google.com/spreadsheets/d/1XyGv34ix2nLOAbrTB7sAwAUinyxkjki9/export?format=csv&gid=1901615913#gid=1901615913'
json_data_path = 'score.json'
data_output_path = 'score_result.json'
data = get_data_json(json_data_path)

df = get_data_google_sheet(url_julong)
# print(df)

section_list = data.keys()
# print(section_list)
for section in section_list:
    data = set_data(section, data, my_config, df)

with open(data_output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f)