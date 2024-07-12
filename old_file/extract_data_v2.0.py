import pandas as pd
import json
import copy

# 设置df显示所有的行和列
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def get_data_google_sheet(url):
    url_julong = url.replace('/edit?gid=', '/export?format=csv&gid=')
    # worksheet = 'Copy of 100指数'
    # 根据链接，从google sheet读取数据
    df = pd.read_csv(url_julong, header=3)
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

def set_data(section, data, df):
    # 设置所需信息的起始行，终行为起始行+9
    config = {
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
    # 
    language_list = ['china','indonesia','double']
    # 数据在df中的位置， 和在json中的位置
    col_data = {
        'pev':{ 'col':4, 'index': 3},
        'pred':{ 'col':5, 'index': 4},
        'real':{ 'col':6, 'index': 5},
        'score':{ 'col':8, 'index': 6},
        'analyze':{ 'col':7, 'index': 7}
    }
    # 每个指标的数据的起始行
    start_row = config[section]['start_row']
    # 遍历一个section的10条指标数据，区分数据中的语言，将数据放入指定位置
    for i in range(0, 10):
        start_row_temp = start_row + i
        for key in col_data.keys():
            data_temp = df.iloc[start_row_temp, col_data[key]['col']]
            index_list = col_data[key]['index']
            if key == 'score':
                data_temp = int(data_temp)
            else:
                data_temp = str(data_temp)
                if len(data_temp.split('\n\n')) != 1:
                    data_temp = data_temp.split('\n\n')
                    data['china'][section][i][index_list] = data_temp[1]
                    data['indonesia'][section][i][index_list] = data_temp[0]
                    data['double'][section][i][index_list] = data_temp[0] + '\n' + data_temp[1]
                    continue
            data['china'][section][i][index_list] = data_temp
            data['indonesia'][section][i][index_list] = data_temp
            data['double'][section][i][index_list] = data_temp
            

# 设置goole sheet的链接，一个链接对应一个表
urls_julong = {
    'week1' : f'https://docs.google.com/spreadsheets/d/1XyGv34ix2nLOAbrTB7sAwAUinyxkjki9/edit?gid=1576425941#gid=1576425941',
    'week2' : f'https://docs.google.com/spreadsheets/d/1XyGv34ix2nLOAbrTB7sAwAUinyxkjki9/edit?gid=472602025#gid=472602025',
    'week3' : f'https://docs.google.com/spreadsheets/d/1XyGv34ix2nLOAbrTB7sAwAUinyxkjki9/edit?gid=390619642#gid=390619642',
    'week4' : f'https://docs.google.com/spreadsheets/d/1XyGv34ix2nLOAbrTB7sAwAUinyxkjki9/edit?gid=105605442#gid=105605442',
    'month' : f'https://docs.google.com/spreadsheets/d/1XyGv34ix2nLOAbrTB7sAwAUinyxkjki9/edit?gid=105605442#gid=105605442'
    }
# 设置数据结构的文件路径
json_data_path = 'score_template.json'
# 设置数据要输出到的文件路径
data_output_path = 'score_result.json'
# 从模板文件中读取模板数据
data_template = get_data_json(json_data_path)
# 预先定义总数据
data = {"week1":{}, "week2":{}, "week3":{}, "week4":{}, "month":{}} 

# 遍历每个文件链接，获取数据，并聚合到总数据
for url_key in urls_julong.keys():
    # 从url中获取数据，存入df
    df = get_data_google_sheet(urls_julong[url_key])
    section_list = data_template['china'].keys()
    # 遍历每个部门的数据，分别将各部门数据存入模板数据
    for section in section_list:
        set_data(section, data_template, df)
        # 将该文件数据存入总数据
    data[url_key] = copy.deepcopy(data_template)

# 将数据写入输出文件
with open(data_output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f)