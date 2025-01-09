import pandas as pd
import json
import copy
import re
import math
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
    df = df.loc[0:109]
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
            # 判断现在是哪个section
            section = section_list[index_section_list]
            # 小标题相对于大标题的行号
            index_sub = index_df - section_start_row - 1
            # 设置数据，根据‘\n\n’分离中文和印尼语
            for index_data in range(4,10):
                # 跳过分数数据 和 评分标准数据
                if index_data == 8 or index_data == 7:
                    continue
                data_temp = df.iloc[index_df,index_data+1]
                if pd.isnull(data_temp):
                    continue
                # 根据'\n\n'和'\r\n\r\n'分离中文和印尼语
                if len(str(data_temp).split('\n\n')) == 2:
                    data_temp = str(data_temp).split('\n\n')
                    data['china'][section]['sub'][index_sub][index_data] = data_temp[1]
                    data['indonesia'][section]['sub'][index_sub][index_data] = data_temp[0]
                    data['double'][section]['sub'][index_sub][index_data] = data_temp[0] + '\n' + data_temp[1]
                elif len(str(data_temp).split('\r\n\r\n')) == 2:
                    data_temp = str(data_temp).split('\r\n\r\n')
                    data['china'][section]['sub'][index_sub][index_data] = data_temp[1]
                    data['indonesia'][section]['sub'][index_sub][index_data] = data_temp[0]
                    data['double'][section]['sub'][index_sub][index_data] = data_temp[0] + '\n' + data_temp[1]
                else:
                    for language in language_list:
                        data[language][section]['sub'][index_sub][index_data] = str(data_temp)

            # 因为分数一栏不用分离中文和印尼语 单独设置分数一栏
            # data_temp = df.iloc[index_df, 9]
            # if (~np.isnan(data_temp)) and len(str(data_temp).strip())>0:
            #     for language in language_list:
            #         data[language][section]['sub'][index_sub][8] = int(data_temp)
            
            # 根据分数算法 得到分数 
            cara_nilai = data['china'][section]['sub'][index_sub][7]
            prev = data['china'][section]['sub'][index_sub][4]
            est = data['china'][section]['sub'][index_sub][5]
            act = data['china'][section]['sub'][index_sub][6]

            nilai = calculate_score(cara_nilai, prev, est, act)

            for language in language_list:
                data[language][section]['sub'][index_sub][8] = nilai

            # 
            index_df += 1
    
    return data
# 根据分数算法 得到分数
def calculate_score(cara_nilai, prev, est, act ):
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
    elif cara_nilai == '小于预测值':
        if est != '_' and act != '_':
            est = digit_string_convert(est)
            act = digit_string_convert(act)
            if est != None and act != None:
                if ~isinstance(est, list) and ~isinstance(act, list):
                    if act < est:
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
    elif cara_nilai == '大于等于预测值\n的90%以上':
        if est != '_' and act != '_':
            est = digit_string_convert(est)
            act = digit_string_convert(act)
            if est != None and act != None:
                if ~isinstance(est, list) and ~isinstance(act, list):
                    if math.isclose(act,est*0.9) or act > est*0.9:
                        nilai = 1
                        return nilai
    elif cara_nilai == '高于预测值':
        if est != '_' and act != '_':
            est = digit_string_convert(est)
            act = digit_string_convert(act)
            if est != None and act != None:
                if ~isinstance(est, list) and ~isinstance(act, list):
                    if act > est:
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
    elif cara_nilai == '大于等于前值\n(可以接受-10%的差异)':
        if prev!= '_' and act!= '_':
            prev = digit_string_convert(prev)
            act = digit_string_convert(act)
            if prev!= None and act!= None:
                if ~isinstance(prev, list) and ~isinstance(act, list):
                    if (math.isclose(act,prev*1.1) or act < prev*1.1) and (math.isclose(act,prev*0.9) or act > prev*0.9):
                        nilai = 1
                        return nilai
    elif cara_nilai == '不为零且大于等于前值':
        if prev != '_' and act != '_':
            prev = digit_string_convert(prev)
            act = digit_string_convert(act)
            if prev != None and act != None:
                if act == 0:
                    nilai = 0
                    return nilai
                elif ~isinstance(prev, list) and ~isinstance(act, list):
                    if act >= prev:
                        nilai = 1
                        return nilai
    elif cara_nilai == '大于等于85%':
        if act != '_':
            act = digit_string_convert(act)
            if act != None:
                if ~isinstance(act, list):
                    if act >= 85:
                        nilai = 1
                        return nilai
    elif cara_nilai == '大于等于70%':
        if act != '_':
            act = digit_string_convert(act)
            if act != None:
                if ~isinstance(act, list):
                    if act >= 70:
                        nilai = 1
                        return nilai
    elif cara_nilai == '小于等于3%':
        if act != '_':
            act = digit_string_convert(act)
            if act != None:
                if ~isinstance(act, list):
                    if act <= 3:
                        nilai = 1
                        return nilai   
    elif cara_nilai == '等于0':
        if act != '_':
            act = digit_string_convert(act)
            if act != None:
                if ~isinstance(act, list):
                    if act == 0:
                        nilai = 1
                        return nilai   
    elif cara_nilai == '大于等于1M':
        if act != '_':
            act = digit_string_convert(act)
            if act != None:
                if ~isinstance(act, list):
                    if act >= 1000000:
                        nilai = 1
                        return nilai   
    
    nilai = 0
    return nilai

# 将数值字符串转换为数值
def digit_string_convert(string):

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

if __name__ == '__main__':

    title_path = os.path.join(os.path.dirname(__file__),'title_result.json')

    # ！！！！！ 阶段性修改周期变量
    url_data_sheet = {
        '2024':{
            '7':{
                'week3':'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1606022133#gid=1606022133',
                'week4':'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=99779159#gid=99779159'
            },
            '8':{
                'week1': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1863606923#gid=1863606923',
                'week2': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1522977825#gid=1522977825',
                'week3': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=410993782#gid=410993782',
                'week4': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1003136681#gid=1003136681',
                'week5': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1947397763#gid=1947397763'
            },
            '9':{
                'week1': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=572236973#gid=572236973',
                'week2': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=319709617#gid=319709617',
                'week3': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=81003741#gid=81003741',
                'week4': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=562058111#gid=562058111'
            },
            '10':{
                'week1': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1552482227#gid=1552482227',
                'week2': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1629294089#gid=1629294089',
                'week3': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=520130035#gid=520130035',
                'week4': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=885897578#gid=885897578',
                'week5': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1480465903#gid=1480465903'
            },
            '11' :{
                'week1': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=595446556#gid=595446556',
                'week2': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1391096319#gid=1391096319',
                'week3': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1096564764#gid=1096564764',
                'week4': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=446467112#gid=446467112'
            },
            '12' :{
                'week1': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1894054535#gid=1894054535',
                'week2': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1320592960#gid=1320592960',
                'week3': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1189307430#gid=1189307430',
                'week4': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=754452638#gid=754452638',
                'week5':'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=545095870#gid=545095870'
            }
        },
        '2025':{
            '1':{
                'week1':'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=545095870#gid=545095870'
            }
        }
        
    }


    output_file = os.path.join(os.path.dirname(__file__),'data_result.json')

    # ！！！！！ 阶段性修改周期变量
    df = extract_google_sheet(url_data_sheet['2024']['12']['week5'])
    # print(df)
    template = get_title_json(title_path)
    data = set_data_title(template, df)
    data_to_json(data, output_file)
