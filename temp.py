# -*- coding: UTF-8 -*- 
 
import re

# Rp. 123,123,123.12
# 6%V37.5%
# -6%
def digit_string_to_float(string):

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

if __name__ == '__main__':
    # string = '-6%V5%'
    # value = digit_string_to_float(string)
    print(len(23))