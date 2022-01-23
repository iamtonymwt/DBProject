from data_standard import dataStandard
from location_coder import lCoder
# from 艺龙爬虫 import yilongCrawler
from 途牛爬虫 import tuniuCrawler
# from 驴妈妈爬虫 import lvmamaCrawler
import time
webList = ['艺龙','途牛','驴妈妈']
#1229
date = time.strftime("%m%d", time.localtime())

if __name__ == '__main__':
    # yilongCrawler(date)
    tuniuCrawler(date)
    # lvmamaCrawler(date)
    # hotelExcelList = ['艺龙 hotel '+date+'.xlsx', '途牛 hotel '+date+'.xlsx','驴妈妈 hotel '+date+'.xlsx']
    # newhotelExcelList = ['艺龙 hotel '+date+'new.xlsx', '途牛 hotel '+date+'new.xlsx','驴妈妈 hotel '+date+'new.xlsx']
    # roomExcelList = ['艺龙 room '+date+'.xlsx', '途牛 room '+date+'.xlsx','驴妈妈 room '+date+'.xlsx']
    hotelExcelList = ['tuniu_hotel_'+date]
    newhotelExcelList = ['tuniu_hotel_'+date+'new']
    roomExcelList = ['tuniu_rooms_'+date]
    lCoder(hotelExcelList)
    dataStandard(newhotelExcelList, roomExcelList)