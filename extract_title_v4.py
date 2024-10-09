import pandas as pd
import json
import os

def extract_google_sheet(url):
    # 设置df显示所有的行和列
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    # 编辑url为需要的格式
    url = url.replace('/edit?gid=', '/export?format=csv&gid=')
    # url += f'&timestamp={int(time.time())}'
    # print(url)
    
    # 根据链接，从google sheet读取数据
    df = pd.read_csv(url, header=3)
    df = df.loc[0:109]
    # 处理数据
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    # 将空值置为0
    df = df.fillna(0)
    # 转换数据类型
    # df = df.astype({'前值': int, '预测值': int, '实际值': int, 'Nilai\n分数':int})
    # 删除最后一行备注
    df = df.drop(df[df['No\n序号'] == '备注：'].index)
    return df

def create_title_data(df):
    section_list = ['human_resource','finance','material','agriculture','industry',
      'commerce', 'big_data','internet','ai','legal']
    language_list = ['china', 'indonesia', 'double']
    # data 声明
    data = {}
    # 初始化data的数据结构
    for language in language_list:
        data[language] = {}
        data[language]['title'] = {}
        for section in section_list:
            data[language][section] = {'title': '', 'PIC': '','sekre': '', 'sub': []}
    # 
    data['china']['title']['subtitle'] = ["序号","分项","负责人","单位","前值","预测值","实际值","分数"]
    data['indonesia']['title']['subtitle'] = ["No","Deskripsi","PIC","Satuan","Prev.","Est.","Act.","Nilai"]
    data['double']['title']['subtitle'] = ["No 序号","Deskripsi 分项","PIC 负责人","Satuan单位","Prev. 前值","Est. 预测值","Act. 实际值","Nilai 分数"]

    data['china']['title']['title'] = '聚龙健康100指数'
    data['indonesia']['title']['title'] = '100 Indikator sehat Julong'
    data['double']['title']['title'] = '100 Indikator sehat Julong\n聚龙健康100指数'

    # 配置循环中需要的标识符
    index_df = 0  # df结构中的行
    index_section_list = -1 # 当前section在section_list中的位置，用来判断当前的section
    section_start_row = 0 # 当前section的起始行，用来判断sub行在section中的位置

    while index_df < len(df):
        # 获取index列的值，通过该列的值，判断当前行是sub小标题还是大标题
        index_value = int(df.iloc[index_df, 0])
        # 如果是大标题
        if index_value != 0:
            # 设置section的起始行
            index_section_list += 1
            section_start_row = index_df
            # 判断现在是哪个section
            section = section_list[index_section_list]
            # 如果为大标题行，先设置大标题和PIC,和负责的秘书
            # 设置大标题
            title_section = str(df.iloc[index_df, 1]).split('\n')
            data['china'][section]['title'] = title_section[1]
            data['indonesia'][section]['title'] = title_section[0]
            data['double'][section]['title'] = str(df.iloc[index_df,1])
            # 设置PIC
            PIC_section = str(df.iloc[index_df, 3]).split('\n')
            data['china'][section]['PIC'] = PIC_section[1]
            data['indonesia'][section]['PIC'] = PIC_section[0]
            data['double'][section]['PIC'] = str(df.iloc[index_df, 3])
            # 设置秘书
            sekre_section = str(df.iloc[index_df, 11]).split('\n')
            data['china'][section]['sekre'] = sekre_section[1]
            data['indonesia'][section]['sekre'] = sekre_section[0]
            data['double'][section]['sekre'] = str(df.iloc[index_df, 11])
            # 跳过一行
            index_df += 1
        # 如果是sub小标题
        elif index_value == 0: 
            # 如果不是大标题行，则写入小标题（分项）、每项负责人PIC
            # 判断现在是哪个section
            section = section_list[index_section_list]
            # 判断当前行相对于大标题的位置, 计算出索引值
            index_sub = index_df - section_start_row - 1
            
            for language in language_list:
                # 扩充sub列表
                data[language][section]['sub'].append(['','','','','','','','',0,''])
                # 写入sub行号， index_sub+1
                data[language][section]['sub'][index_sub][0] = index_sub + 1
            
            # 写入小标题
            subtitle_section = str(df.iloc[index_df, 2]).split('\n')
            if len(subtitle_section) == 2:
                data['china'][section]['sub'][index_sub][1] = subtitle_section[1]
                data['indonesia'][section]['sub'][index_sub][1] = subtitle_section[0]
                data['double'][section]['sub'][index_sub][1] = str(df.iloc[index_df, 2])
            elif len(subtitle_section) == 1:
                for language in language_list:
                    data[language][section]['sub'][index_sub][1] = subtitle_section[0]

            # 写入每项负责人PIC
            PIC_section = str(df.iloc[index_df, 3]).split('\n')
            if len(PIC_section) == 2:
                data['china'][section]['sub'][index_sub][2] = PIC_section[1]
                data['indonesia'][section]['sub'][index_sub][2] = PIC_section[0]
                data['double'][section]['sub'][index_sub][2] = str(df.iloc[index_df, 3])
            elif len(PIC_section) == 1:
                for language in language_list:
                    data[language][section]['sub'][index_sub][2] = PIC_section[0]    

            # 写入每项单位
            satuan_section = str(df.iloc[index_df, 4])
            if satuan_section == '0':
                for language in language_list:
                    data[language][section]['sub'][index_sub][3] = '-'
            else :
                satuan_section = satuan_section.split('\n')
                if len(satuan_section) == 2:
                    data['china'][section]['sub'][index_sub][3] = satuan_section[1]
                    data['indonesia'][section]['sub'][index_sub][3] = satuan_section[0]
                    data['double'][section]['sub'][index_sub][3] = str(df.iloc[index_df, 4])
                elif len(satuan_section) == 1:
                    for language in language_list:
                        data[language][section]['sub'][index_sub][3] = satuan_section[0]

            # 写入每项算分方法
            cara_nilai = str(df.iloc[index_df, 8])
            if cara_nilai == '0':
                for language in language_list:
                    data[language][section]['sub'][index_sub][7] = '-'
            else :
                for language in language_list:
                    data[language][section]['sub'][index_sub][7] = cara_nilai
                    
            index_df += 1
    return data

def data_to_json(data, output_file):
    # 将数据写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)
# excel_url = 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1901615913#gid=1901615913'


if __name__ == '__main__':

    excel_url = {
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
            'week1': 'https://docs.google.com/spreadsheets/d/1LpX1tkuI7rgntZPLhsXONYjqmxRJPiYA/edit?gid=1552482227#gid=1552482227'
        }
    }
    output_json_file = os.path.join(os.path.dirname(__file__),'title_result.json')
    df = extract_google_sheet(excel_url['10']['week1'])
    # print(df)
    # print(len(df))
    data = create_title_data(df)
    # print(data)
    data_to_json(data, output_json_file)
