import xlsxwriter as xw
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import  TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote
import time,random,os,win32api,win32con

options = webdriver.ChromeOptions()
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')
# options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
browser = webdriver.Chrome(chrome_options=options)
browser.set_page_load_timeout(3)
wait = WebDriverWait(browser,12)

hotels_table = []
rooms_table = []

def stopLoading():
    win32api.keybd_event(27,0,0,0)
    win32api.keybd_event(27,0,win32con.KEYEVENTF_KEYUP,0)
    return

def renew(page):
    print('正在爬取第',page,'页')
    try:
        if page == 1:
            url = 'http://s.lvmama.com/hotel/U13C20211225O20211226?keyword=&mdd=%E5%8C%97%E4%BA%AC&losc=332212&ict=i#list'
            try:
                browser.get(url)
            except:
                stopLoading()
        # browser.refresh()
        stopLoading()
        time.sleep(2)

        #main window info
        html = browser.page_source
        doc = pq(html)
        # items = doc('#mainsrp-itemlist .items .item').items()
        time.sleep(3)
        items = doc('.prdLi.clearfix   ').items()
        items = list(items)
        hotels = browser.find_elements_by_class_name('proImg')

        for i in range(15):
            #main window info
            hotel = get_hotel_info(i, items)
            #rooms info & more
            hotel_name = hotel['name']
            time.sleep(1)
            hotels[i].click()
            time.sleep(3)
            windows = browser.window_handles
            browser.switch_to.window(windows[-1])
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
            # with open('hotel.txt','a',encoding='utf-8') as f:
            #     f.write(str(hotel))
            #     f.write(str(rooms))
            #     f.write('\n')

        windows = browser.window_handles
        browser.switch_to.window(windows[-1])
        time.sleep(1)
        button = browser.find_element_by_class_name('nextpage')
        button.click()

    except TimeoutException:
        renew(page)

 
def get_hotel_info(i,items):   #提取商品数据
    hotel = {
        'image':items[i].find('.proImg img').attr('src'),   #商品图片
        'name':items[i].find('.proTit a').attr('title'),   #名字
        'type':items[i].find('.proTit .djjd_tagsclasses').text(),   #类别
        'price':items[i].find('.priceInfo-price').text(),          #价格
        'mark':items[i].find('.product-number li a b').text(),      #评分
        'remark':"真的好",       #评价
        'deal':"暂无订单信息",     #付款人数
        'location':items[i].find('.proInfo-address i').text()#地址
    }
    print(hotel)
    return hotel

def get_room_info(hotel_name):
    stopLoading()
    html_room = browser.page_source
    doc_room = pq(html_room)
    # address = doc_room.find('.address-box .desc').text()
    # items = doc('#mainsrp-itemlist .items .item').items()
    rooms = doc_room('.room_list.roomList').items()
    rooms = list(rooms)
    room_info = []
    for room in rooms:
        room = {
            'hotel_name':hotel_name,
            'type':room.find('dl dt h4').text(),
            'price':room.find('.roomList-price').text(),
        }
        if (room['type'] == ''):
            continue
        if (room['price'] == '') :
            room['price'] = room.find('.roomList-price.saleoff').text()
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


def lvmamaCrawler(date):
    for i in range(1,2):
        try:
            renew(i)
            time.sleep(1)
        except BaseException:
            continue
    hotel_toExcel(hotels_table, '驴妈妈 hotel '+date+'.xlsx')
    room_toExcel(rooms_table, '驴妈妈 rooms '+date+'.xlsx')

if __name__ == '__main__':
    for i in range(1,2):
        try:
            renew(i)
            time.sleep(1)
        except BaseException:
            continue
    hotel_toExcel(hotels_table, '驴妈妈 hotel 1225.xlsx')
    room_toExcel(rooms_table, '驴妈妈 rooms 1225.xlsx')

 