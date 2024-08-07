import pandas as pd
import json

'''
    将构造好的data数据存入总json文件
'''

def init_data_json(total_data_path):
    data = {
        '2024' : {
            '7': {
                'week1':{}
            }
        }
    }
    write_total_data(total_data_path,data)


def get_total_data(total_data_path):
    with open(total_data_path, 'r', encoding='utf-8') as f:
        total_data = json.load(f)
    return total_data

def get_data(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_total_data(total_data_path,total_data):
    with open(total_data_path, 'w', encoding='utf-8') as f:
        json.dump(total_data, f)

if __name__ == '__main__':
    total_data_path = 'total_data.json'
    data_path = 'data_result.json'
    total_data = get_total_data(total_data_path)
    data = get_data(data_path)
    total_data['2024']['7']['week5'] = data
    write_total_data(total_data_path,total_data)