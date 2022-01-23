#crawed data standard
import xlsxwriter as xw
import xlrd
import pandas as pd
import requests
import time
import re
import random

# hotelList = ['艺龙 hotel 1228new']
# roomList = ['艺龙 rooms 1228']

# hotelList = ['驴妈妈 hotel 1210new','驴妈妈 hotel 1217new','驴妈妈 hotel 1225new']
# roomList = ['驴妈妈 rooms 1210','驴妈妈 rooms 1217','驴妈妈 rooms 1225']

# hotelList = ['途牛 hotel 1210new','途牛 hotel 1217new','途牛 hotel 1225new']
# roomList = ['途牛 rooms 1210','途牛 rooms 1217','途牛 rooms 1225']

def standardHotelData(hotelList):
    for hotelName in hotelList:
        data_path = hotelName +'.xlsx'   #设置文件路径
        data=pd.read_excel(data_path)   #通过read_excel()读取文件，内容存在data中
        for i in range(len(data)):
            try:
                ##price
                ori = data.iloc[i,3]
                matchObj = re.match( r'.*?(\d+).*', ori, re.M|re.I)
                data.iloc[i,3] = matchObj.group(1)
                ##mark
                ori = data.iloc[i,4]
                matchObj = re.match( r'.*?(\d+\.\d+).*', ori, re.M|re.I)
                data.iloc[i,4] = matchObj.group(1)
                #deal
                ori = data.iloc[i,6]
                matchObj = re.match( r'.*?(\d+).*', ori, re.M|re.I)
                data.iloc[i,6] = matchObj.group(1)
            except:
                data.iloc[i,3] = 313
                data.iloc[i,4] = 4.13
                data.iloc[i,6] = 113
        data.to_excel(hotelName[:-3]+'final.xlsx', index = False)  #保存excel文件
def standardRoomData(roomList):
    for roomName in roomList:
        data_path = roomName +'.xlsx'   #设置文件路径
        data=pd.read_excel(data_path)   #通过read_excel()读取文件，内容存在data中
        for i in range(len(data)):
            try:
                ##price
                ori = data.iloc[i,2]
                matchObj = re.match( r'.*?(\d+).*', ori, re.M|re.I)
                data.iloc[i,2] = matchObj.group(1)
            except:
                data.iloc[i,2] = 313
        data.to_excel(roomName+'final.xlsx', index = False)  #保存excel文件

def dataStandard(hotelList, roomList):
    standardHotelData(hotelList)
    standardRoomData(roomList)

if __name__ == '__main__':
    standardHotelData()
    standardRoomData()
