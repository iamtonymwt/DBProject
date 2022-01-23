# location_coder
import xlsxwriter as xw
import xlrd
import pandas as pd
import requests
import time
import re
import random

# excelList = ['驴妈妈 hotel 1210', '驴妈妈 hotel 1217', '驴妈妈 hotel 1225']
# excelList = ['途牛 hotel 1210', '途牛 hotel 1217', '途牛 hotel 1225']
# excelList = ['艺龙 hotel 1228']

def addressToLocation(address):
    """
    将地址转换为经纬度
    :param address: 地址
    :return: 经度和维度
    """
    # 在高德地图开发者平台（https://lbs.amap.com/）申请的key，需要替换为自己的key
    parameters = {
                    'key': 'd29 xxx ea06fa03fe8e5',
                    'address': address,
                    'city': '北京',
                 }
    base = 'http://restapi.amap.com/v3/geocode/geo?'
    contest = requests.get(base,parameters).json()
    if (len(contest['geocodes'])):
        location = contest['geocodes'][0]['location']
        if location == '':
            location = '116.460507,40.007137'
        #
        # matchObj = re.match( r'(.*),(.*)', location, re.M|re.I)
        # longitude = float(matchObj.group(1)) + random.uniform(-0.01,0.01)
        # latitude = float(matchObj.group(2)) + random.uniform(-0.01,0.01)
        # neolocation = str(longitude)+','+str(latitude)
        #
        return location
    return ''
    
def locationCoder(excelIdent):
    data_path=excelIdent+'.xlsx'   #设置文件路径
    addrs=pd.read_excel(data_path)   #通过read_excel()读取文件，内容存在data中
    addrs.insert(8, '经纬度', '', allow_duplicates=False)
    # print(len(data))
    for i in range(len(addrs)):
        addr = addrs.iloc[i][1]
        location = addressToLocation(addr)
        # time.sleep(0.1)
        if location == '':
            location = '116.460507,40.007137'
        addrs.loc[i,'经纬度'] = location
        # print(addrs.iloc[i]['经纬度'])

    addrs.to_excel(excelIdent+'new.xlsx', index = False)  #保存excel文件

def lCoder(excelList):
        locationCoder(excelList[0])

if __name__ == '__main__':
    excelList = ['艺龙 hotel 1228']
    for excel in excelList:
        locationCoder(excel)