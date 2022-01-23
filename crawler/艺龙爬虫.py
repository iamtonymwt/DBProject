import re
import xlsxwriter as xw
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import  TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote
import time

options = webdriver.ChromeOptions()
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')
# options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
browser = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(browser,12)

hotels_table = []
rooms_table = []

def renew(page):
    print('正在刷新第',page,'次')
    try:
        if page == 1: 
            url = 'https://hotel.elong.com/hotel/hotellist?cityId=0101&city=0101&inDate=2021-12-28&outDate=2021-12-29&filterList=8888_1&pageIndex=1&pageSize=20&t=1640661127516'
            browser.get(url)
            time.sleep(2)
            button = browser.find_element_by_id('login_btn')
            button.click()
            time.sleep(20)
        url = 'https://hotel.elong.com/hotel/hotellist?cityId=0101&pageSize=20&t=1640664552998&city=0101&inDate=2021-12-28&outDate=2021-12-29&filterList=8888_1&pageIndex='+str(page)
        browser.get(url)
        time.sleep(2)

        #main window info
        html = browser.page_source
        doc = pq(html)
        # items = doc('#mainsrp-itemlist .items .item').items()
        time.sleep(1)
        images = doc('.hotelImg').items()
        images = list(images)
        msgs = doc('.hotelMsg').items()
        msgs = list(msgs)
        infos = doc('.hotelInfo.clearfix').items()
        infos = list(infos)
        clicks = browser.find_elements_by_class_name('hotelName')

        for i in range(15):
            #main window info
            hotel = get_hotel_info(i, images, msgs, infos)
            #rooms info & more
            hotel_name = hotel['name']
            clicks[i].click()
            time.sleep(2)
            windows = browser.window_handles
            browser.switch_to.window(windows[-1])
            time.sleep(1)
            rooms = get_room_info(hotel_name)
            time.sleep(1)
            browser.close()
            time.sleep(1)
            if (len(rooms) == 0):
                windows = browser.window_handles
                browser.switch_to.window(windows[-1])
                time.sleep(1)
                continue
            
            hotels_table.append(hotel)
            rooms_table.extend(rooms)

            windows = browser.window_handles
            browser.switch_to.window(windows[-1])
            time.sleep(1)

    except TimeoutException:
        renew(page)

 
def get_hotel_info(i, images, msgs, infos):   #提取商品数据
    hotel = {
        'image':images[i].find('a img').attr('src'),   #商品图片
        'name':msgs[i].find('.name').attr('title'),   #名字
        'type':msgs[i].find('.hotelName a .otherBox .starLevelStr').text(),   #类别
        'price':infos[i].find('.newPrice').text(),          #价格
        'mark':infos[i].find('.score.mb5 em').text(),      #评分
        'remark':infos[i].find('.key.mb10.ellipsis').attr('title'),       #评价
        'deal':infos[i].find('.comment.mb10').text(),     #付款人数
        'location':msgs[i].find('.position span').text()#地址
    }
    print(hotel)
    return hotel

def get_room_info(hotel_name):
    html_room = browser.page_source
    doc_room = pq(html_room)
    # address = doc_room.find('.address-box .desc').text()
    # items = doc('#mainsrp-itemlist .items .item').items()
    rooms = doc_room('.roomItem').items()
    room_info = []
    for room in rooms:
        price = room.find('.price .nowPri').text()
        try:
            matchObj = re.match( r'(¥.*?)\s.*', price, re.M|re.I)
            price = matchObj.group(1)
        except:
            price = price
        room = {
            'hotel_name':hotel_name,
            'type':room.find('.name').text(),
            'price':price
        }
        room_info.append(room)
    print(room_info)
    return room_info


def hotel_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['酒店图片', '酒店名', '酒店类型','酒店基础价格','酒店评分','酒店评价','评价/消费人数','地址']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        insertData = [data[j]["image"], data[j]["name"],data[j]["type"], data[j]["price"], data[j]["mark"], data[j]["remark"], data[j]["deal"], data[j]["location"]], 
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData[0])
        i += 1
    workbook.close()  # 关闭表

def room_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['所属酒店名','房间类型','房间价格']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        insertData = [data[j]["hotel_name"], data[j]["type"], data[j]["price"]] 
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    workbook.close()  # 关闭表

# price = '¥234'
# matchObj = re.match( r'(¥.*)\s.*', price, re.M|re.I)
# price = matchObj.group(1)

def yilongCrawler(date):
    for i in range(1,2):
        try:
            renew(i)
            time.sleep(1)
        except BaseException:
            continue
    browser.close()
    hotel_toExcel(hotels_table, '艺龙 hotel '+date+'.xlsx')
    room_toExcel(rooms_table, '艺龙 rooms '+date+'.xlsx')

if __name__ == '__main__':
    for i in range(1,2):
        try:
            renew(i)
            time.sleep(1)
        except BaseException:
            continue
    browser.close()
    hotel_toExcel(hotels_table, '艺龙 hotel 1228.xlsx')
    room_toExcel(rooms_table, '艺龙 rooms 1228.xlsx')

 