import json
import copy



def get_data_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        data = json.loads(data)
        return data
    
def set_data_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

if __name__ == '__main__':
    week1_path = 'score_result.json'
    title_path = 'title.json'
    sekre_path = 'data_result.json'
    section_list = ['human_resource','finance','material','agriculture','industry',
      'commerce', 'big_data','internet','ai','legal']
    language_list = ['china', 'indonesia', 'double']
    
    data_week1 = get_data_json(week1_path)['week1']

    data_title = get_data_json(title_path)

    sekre_data = get_data_json(sekre_path)

    data_result = {}
    for language in language_list:
        data_result[language] = {}
        data_result[language]['title'] = {}
        for section in section_list:
            data_result[language][section] = {}
            data_result[language][section]['title'] = data_title[language]["section"][section]['title']
            data_result[language][section]['PIC'] = data_title[language]["section"][section]['PIC']
            data_result[language][section]['sekre'] = sekre_data[language][section]['sekre']
            data_result[language][section]['sub'] = data_week1[language][section]

    data_result['china']['title']['subtitle'] = ["序号","分项","负责人","前值","预测值","实际值","分数"]
    data_result['indonesia']['title']['subtitle'] = ["No","Deskripsi","PIC","Prev.","Est.","Act.","Nilai"]
    data_result['double']['title']['subtitle'] = ["No 序号","Deskripsi 分项","PIC 负责人","Prev. 前值","Est. 预测值","Act. 实际值","Nilai 分数"]

    data_result['china']['title']['title'] = '聚龙健康100指数'
    data_result['indonesia']['title']['title'] = '100 Indikator sehat Julong'
    data_result['double']['title']['title'] = '100 Indikator sehat Julong\n聚龙健康100指数'

    output_path = 'temp.json'
    set_data_json(output_path, data_result)

