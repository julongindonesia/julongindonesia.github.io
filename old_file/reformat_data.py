import json


def data_to_json(data, output_file):
    # 将数据写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def get_data_json(path):
    # 从标题文件中读取数据结构
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        json_data = json.loads(data)
        return json_data

def format_sublist(language_list, section_list, data):
    
    for language in language_list:
        for section in section_list:
            for i in range(0,10):
                data[language][section]['sub'][i][3] = '-'
                data[language][section]['sub'][i][7] = '-'
    



if __name__ == '__main__':
    file_path = 'total_data.json'
    language_list = ['china', 'indonesia', 'double']
    section_list = ['human_resource','finance','material','agriculture','industry',
      'commerce', 'big_data','internet','ai','legal']
    
    total_data = get_data_json(file_path)
    for period in ('week1', 'week2'):
        total_data['2024']['7'][period]['china']['title']['subtitle'] = ['序号', '分项', '负责人', '单位', '前值', '预测值', '实际值', '分数']
        total_data['2024']['7'][period]['indonesia']['title']['subtitle'] = ['No', 'Deskripsi', 'PIC', 'Satuan', 'Prev.', 'Est.', 'Act.', 'Nilai']
        total_data['2024']['7'][period]['double']['title']['subtitle'] = ['No 序号', 'Deskripsi 分项', 'PIC 负责人', 'Satuan 单位', 'Prev. 前值', 'Est. 预测值', 'Act. 实际值', 'Nilai 分 数']

    data_to_json(total_data, file_path)
    # ['序号', '分项', '负责人', '前值', '预测值', '实际值', '分数']
    # ['No', 'Deskripsi', 'PIC', 'Prev.', 'Est.', 'Act.', 'Nilai']
    # ['No 序号', 'Deskripsi 分项', 'PIC 负责人', 'Prev. 前值', 'Est. 预测值', 'Act. 实际值', 'Nilai 分 数']
    # format_sublist(language_list, section_list, data)
    # data_to_json(total_data, file_path)
    
    