# -*- coding: UTF-8 -*- 
 
import re

# Rp. 123,123,123
def Rp_to_int(string):
    singal = re.search('Rp.', string)
    if singal != None:
        value = re.sub(',', '', string)  
        value = int(re.search('\d+', value).group())
        return value
    else:
        return None

# -0.5%    23.1%
def percent_to_float(string):
    singal = re.search('%', string)
    singal2 = re.search('\(', string)
    if singal != None and singal2 == None:
        value = re.search('[-0-9.]+', string).group()
        return float(value)/100
    return None

#  91(0.5%)
def complex_percent_to_float(string):
    singal = re.search('\((.*)%\)',string)
    if singal != None:
        value = singal.group(1)
        return float(value)/100
    return None
# 704.483 / 117.095
def complex_float_to_float(string):
    singal = re.search('(.*) / (.*)', string)
    if singal!= None:
        value = singal.group(1)
        value = float(value)
        return value
    return None

if __name__ == '__main__':
    # string = '704.483 / 117.095'
    # value = complex_float_to_float(string)
    
    print('和预测值进行对比\n（差距10%以内）'.encode('unicode-escape'))
    string = b'\u548c\u9884\u6d4b\u503c\u8fdb\u884c\u5bf9\u6bd4\n\uff08\u5dee\u8ddd10%\u4ee5\u5185\uff09'.decode('unicode-escape')
    print(string == '和预测值进行对比\n（差距10%以内）')