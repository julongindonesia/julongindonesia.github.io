import json
import re
import math

def calculate_score(cara_nilai, prev, est, act ):

    if digit_string_convert(prev) == None or digit_string_convert(est) == None or digit_string_convert(act) == None:
        return 2

    if cara_nilai == '和预测值进行对比\n（差距10%以内）':    
        if est != '_' and act != '_':
            est = digit_string_convert(est)
            act = digit_string_convert(act)
            if est != None and act != None:
                if ~isinstance(est, list) and ~isinstance(act, list):
                    if (math.isclose(act,est*1.1) or act < est*1.1) and (math.isclose(act,est*0.9) or act > est*0.9):
                        nilai = 1
                        return nilai
    elif cara_nilai == '小于等于预测值':
        if est != '_' and act != '_':
            est = digit_string_convert(est)
            act = digit_string_convert(act)
            if est != None and act != None:
                if ~isinstance(est, list) and ~isinstance(act, list):
                    if math.isclose(act,est) or act < est:
                        nilai = 1
                        return nilai
    elif cara_nilai == '大于等于预测值':
        if est != '_' and act != '_':
            est = digit_string_convert(est)
            act = digit_string_convert(act)
            if est != None and act != None:
                if ~isinstance(est, list) and ~isinstance(act, list):
                    if math.isclose(act,est) or act > est:
                        nilai = 1
                        return nilai

    elif cara_nilai == '小于等于前值':
        if prev != '_' and act != '_':
            prev = digit_string_convert(prev)
            act = digit_string_convert(act)
            if prev != None and act != None:
                if ~isinstance(prev, list) and ~isinstance(act, list):
                    if act <= prev:
                        nilai = 1
                        return nilai
    elif cara_nilai == '大于等于前值':
        if prev != '_' and act != '_':
            prev = digit_string_convert(prev)
            act = digit_string_convert(act)
            if prev != None and act != None:
                if ~isinstance(prev, list) and ~isinstance(act, list):
                    if act >= prev:
                        nilai = 1
                        return nilai
    nilai = 0
    return nilai

# 将数值字符串转换为数值
def digit_string_convert(string):
    # 先过滤掉有字母或汉字的值
    singal = re.search('[\u4E00-\u9FFFa-zA-Z\(\)\\/]', string)
    if singal != None:
        return None
    singal = re.search('V',string, re.I)
    if singal!= None:
        values = string.split('V')
        for i in range(0,2):
            value = re.search('[-0-9.]+', values[i]).group()
            values[i] = float(value)/100
        return values
    singal = re.search('%', string)
    if singal != None:
        value = re.search('[-0-9.]+', string).group()
        return float(value)/100
    
    singal = re.search(',',string)
    if singal != None:
        value = re.sub(',', '', string)
        return float(value)
    
    if re.match('^-?\d+.\d+$', string):
        return float(string)
    elif re.match('^-?\d+$', string):
        return int(string)
    else:
        return None

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

def write_algorithm_to_week_before():
    json_path = 'total_data.json'
    data = get_title_json(json_path)
    week1_data = data['2024']['7']['week1']
    week2_data = data['2024']['7']['week2']
    week3_data = data['2024']['7']['week3']

    section_list = ['human_resource','finance','material','agriculture','industry',
      'commerce', 'big_data','internet','ai','legal']
    language_list = ['china', 'indonesia', 'double']

    for language in language_list:
        for section in section_list:
            for i in range(0,10):
                week1_data[language][section]['sub'][i][7] = week3_data[language][section]['sub'][i][7]
                week2_data[language][section]['sub'][i][7] = week3_data[language][section]['sub'][i][7]
                week1_data[language][section]['sub'][i][3] = week3_data[language][section]['sub'][i][3]
                week2_data[language][section]['sub'][i][3] = week3_data[language][section]['sub'][i][3]
    data_to_json(data, json_path)

def reset_score(period):
    json_path = 'total_data.json'
    data = get_title_json(json_path)
    week_data = data['2024']['7'][period]
    
    section_list = ['human_resource','finance','material','agriculture','industry',
      'commerce', 'big_data','internet','ai','legal']
    language_list = ['china', 'indonesia', 'double']

    for section in section_list:
        for index_sub in range(0,10):
            # 根据分数算法 得到分数 
            cara_nilai = week_data['china'][section]['sub'][index_sub][7]
            prev = week_data['china'][section]['sub'][index_sub][4]
            est = week_data['china'][section]['sub'][index_sub][5]
            act = week_data['china'][section]['sub'][index_sub][6]

            nilai = calculate_score(cara_nilai, prev, est, act)
            
            for language in language_list:
                week_data[language][section]['sub'][index_sub][8] = nilai

    data_to_json(data, json_path)


def reset_score_unrule_week2():
    json_path = 'total_data.json'
    data = get_title_json(json_path)
    week2_data = data['2024']['7']['week2']

    section_list = ['human_resource','finance','material','agriculture','industry',
      'commerce', 'big_data','internet','ai','legal']
    language_list = ['china', 'indonesia', 'double']

    for language in language_list:
        week2_data[language]['human_resource']['sub'][4][8] = 0
        week2_data[language]['human_resource']['sub'][5][8] = 1

        week2_data[language]['finance']['sub'][0][8] = 1
        week2_data[language]['finance']['sub'][1][8] = 1
        week2_data[language]['finance']['sub'][2][8] = 1
        week2_data[language]['finance']['sub'][5][8] = 0
        week2_data[language]['finance']['sub'][6][8] = 0
        week2_data[language]['finance']['sub'][8][8] = 0
        week2_data[language]['finance']['sub'][9][8] = 1

        week2_data[language]['material']['sub'][6][8] = 0
        week2_data[language]['material']['sub'][8][8] = 0
        week2_data[language]['material']['sub'][9][8] = 1

        week2_data[language]['agriculture']['sub'][3][8] = 1
        week2_data[language]['agriculture']['sub'][6][8] = 1
        week2_data[language]['agriculture']['sub'][8][8] = 0
        
        week2_data[language]['industry']['sub'][0][8] = 0
        week2_data[language]['industry']['sub'][1][8] = 0
        week2_data[language]['industry']['sub'][5][8] = 1
        week2_data[language]['industry']['sub'][6][8] = 1
        week2_data[language]['industry']['sub'][9][8] = 0

        week2_data[language]['commerce']['sub'][0][8] = 1
        week2_data[language]['commerce']['sub'][1][8] = 0
        week2_data[language]['commerce']['sub'][2][8] = 1
        week2_data[language]['commerce']['sub'][3][8] = 0
        week2_data[language]['commerce']['sub'][5][8] = 0
        week2_data[language]['commerce']['sub'][8][8] = 1

        week2_data[language]['ai']['sub'][1][8] = 0
        week2_data[language]['ai']['sub'][2][8] = 1
        week2_data[language]['ai']['sub'][3][8] = 0
        week2_data[language]['ai']['sub'][4][8] = 1

        week2_data[language]['legal']['sub'][4][8] = 0
        week2_data[language]['legal']['sub'][5][8] = 1
        week2_data[language]['legal']['sub'][7][8] = 1
        week2_data[language]['legal']['sub'][9][8] = 1

    data_to_json(data, json_path)

def reset_score_unrule_week1():
    json_path = 'total_data.json'
    data = get_title_json(json_path)
    week1_data = data['2024']['7']['week1']

    section_list = ['human_resource','finance','material','agriculture','industry',
      'commerce', 'big_data','internet','ai','legal']
    language_list = ['china', 'indonesia', 'double']

    for language in language_list:
        week1_data[language]['finance']['sub'][1][8] = 1
        week1_data[language]['finance']['sub'][2][8] = 1
        week1_data[language]['finance']['sub'][6][8] = 1
        week1_data[language]['finance']['sub'][8][8] = 0
        week1_data[language]['finance']['sub'][9][8] = 1

        week1_data[language]['material']['sub'][0][8] = 0
        week1_data[language]['material']['sub'][2][8] = 0
        week1_data[language]['material']['sub'][5][8] = 1
        week1_data[language]['material']['sub'][6][8] = 1
        week1_data[language]['material']['sub'][7][8] = 1

        week1_data[language]['industry']['sub'][0][8] = 0
        week1_data[language]['industry']['sub'][1][8] = 0
        week1_data[language]['industry']['sub'][5][8] = 0
        week1_data[language]['industry']['sub'][8][8] = 0
        week1_data[language]['industry']['sub'][9][8] = 0

        week1_data[language]['commerce']['sub'][0][8] = 1
        week1_data[language]['commerce']['sub'][1][8] = 0
        week1_data[language]['commerce']['sub'][2][8] = 0
        week1_data[language]['commerce']['sub'][3][8] = 0
        week1_data[language]['commerce']['sub'][4][8] = 0
        week1_data[language]['commerce']['sub'][5][8] = 0
        week1_data[language]['commerce']['sub'][6][8] = 0
        week1_data[language]['commerce']['sub'][7][8] = 1
        week1_data[language]['commerce']['sub'][8][8] = 0
        week1_data[language]['commerce']['sub'][9][8] = 0

        week1_data[language]['ai']['sub'][1][8] = 1
        week1_data[language]['ai']['sub'][3][8] = 1
        week1_data[language]['ai']['sub'][4][8] = 0

        week1_data[language]['legal']['sub'][4][8] = 0
        week1_data[language]['legal']['sub'][5][8] = 1
        week1_data[language]['legal']['sub'][7][8] = 1
        week1_data[language]['legal']['sub'][9][8] = 1

    data_to_json(data, json_path)

if __name__ == '__main__':
    reset_score_unrule_week1()