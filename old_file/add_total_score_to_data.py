import json

def data_to_json(data, output_file):
    # 将数据写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def get_title_json(title_path):
    # 从标题文件中读取数据结构
    with open(title_path, 'r', encoding='utf-8') as f:
        data = f.read()
        json_data = json.loads(data)
        return json_data

if __name__ == '__main__':
    file_path = 'total_data.json'

    period_list = ['week1', 'week2', 'week3']

    data = get_title_json(file_path)

    section_list = ['human_resource','finance','material','agriculture','industry',
      'commerce', 'big_data','internet','ai','legal']
    language_list = ['china', 'indonesia', 'double']

    for period in period_list:
        data_period = data['2024']['7'][period]
        for language in language_list:
            for section in section_list:
                score = 0
                for index in range(0,10):
                    score += data_period[language][section]['sub'][index][8]
                data_period[language][section]['score'] = score
    
    for period in period_list:
        data_period = data['2024']['7'][period]
        for language in language_list:
            total_score = 0
            for section in section_list:
                total_score += data_period[language][section]['score']
            data_period[language]['title']['total_score'] = total_score

    data_to_json(data, file_path)



