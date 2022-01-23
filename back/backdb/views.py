import json
import xlrd
from django.db.models import Q
from django.http import JsonResponse
import sys
from numpy import *
import numpy as np
import random
# Create your views here.
from rest_framework import viewsets
import requests
import json

from backdb.models import *
from backdb.serializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def login(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    email = body_dict.get('mail')
    password = body_dict.get('password')
    info = None
    code = 0
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        if user.password == password:
            code = 200
            msg = "登录成功"
            info = user.to_dict()
            info['type'] = 2
            info['loc_hotel'] = {}
        else:
            code = 402
            msg = "密码错误"
    elif Business.objects.filter(email=email).exists():
        business = Business.objects.get(email=email)
        if business.password == password:
            code = 200
            msg = "登录成功"
            info = business.to_dict()
            info['type'] = 1
            if Hotel.objects.filter(business_id=business.id).exists():
                dic = Hotel.objects.filter(business_id=business.id).first().to_dict()
                dic['comid'] = business.id
                dic['room'] = [{'id': 1, 'type': '单人间', '总量': 150, '已预约': 55, 'price': 123}, {'id': 2, 'type':'双人间', '总量': 150, '已预约': 131, 'price': 133}],
                dic['roomInfo'] = {'single': {'amount': 150, 'subscribed': 45, 'price': 123},
                          'double': {'amount': 150, 'subscribed': 131, 'price': 133},
                          'triple': None},
                dic['regTime'] = '2021-12-3'
                info['loc_hotel'] = dic
            else:
                info['loc_hotel'] = {}
        else:
            code = 402
            msg = "密码错误"
    else:
        code = 404
        msg = "不存在此用户/商家"
    data = {'code': code, 'msg': msg, "userInfo": info}
    resp = JsonResponse(dict(data))
    return resp

## TODO

## finish


def user(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    name = body_dict.get('username')
    email = body_dict.get('email')
    password = body_dict.get('password')
    # date =
    type = body_dict.get('type')
    print(type)
    # 用户
    if type == '1':
        if User.objects.filter(email=email).exists():
            code = 404
            msg = "留言内容包含非法字符"
        else:
            code = 200
            msg = '注册成功'
            User.objects.create(name=name, email=email, password=password)
    # 商家
    elif type == '2':
        if Business.objects.filter(email=email).exists():
            code = 404
            msg = "此邮箱已注册"
        else:
            code = 200
            msg = '注册成功'
            Business.objects.create(name=name, email=email, password=password)
    else:
        print('type error')
        code = 404
        msg = "type error"

    data = {'code':code, 'msg':msg}
    resp = JsonResponse(dict(data))
    return resp

## TODO
def updateUser(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    id = body_dict.get('id')
    email = body_dict.get('email')
    name = body_dict.get('username')
    password = body_dict.get('password')
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
    else:
        user = Business.objects.get(email=email)
    if password == '':
        user.name = name
        user.save()
    ## 修改密码
    else:
        pass
    data = {'code': 200, 'msg': '修改用户信息成功'}
    resp = JsonResponse(dict(data))
    return resp

def loadExcel(request):
    wb = xlrd.open_workbook("D:\用户\桌面\数据库\途牛 rooms 1225final.xlsx")
    table = wb.sheets()[0]
    date = "2021-12-25"
    # for i in range(1, table.nrows):
    #     j = 0
    #     pic = table.row_values(i)[1+j]
    #     name = table.row_values(i)[2+j]
    #     type = table.row_values(i)[3+j]
    #     price = table.row_values(i)[4+j]
    #     score = table.row_values(i)[5+j]
    #     sales = table.row_values(i)[7+j]
    #     addr = table.row_values(i)[8+j]
    #     longlatitude = table.row_values(i)[9+j]
    #     platform = table.row_values(i)[10+j]
    #     if not Hotel.objects.filter(Q(name=name) & Q(platform_id=platform)).exists():
    #         Hotel.objects.create(price=price, sales=sales, name=name, address=addr, picture=pic, longlatitude=longlatitude, platform_id=platform, score=score, type=type)
    #     else:
    #         hotel = Hotel.objects.get(Q(name=name) & Q(platform_id=platform))
    #         hotel.picture = pic
    #         hotel.type = type
    #         hotel.score = score
    #         hotel.price = price
    #         hotel.sales = sales
    #         hotel.save()
    #     HotelDetail.objects.create(name=name, date=date, price=price, sales=sales, score=score, platform_id=platform)
    for i in range(1, table.nrows):
        j = 0
        hotel_name = table.row_values(i)[j+1]
        type = table.row_values(i)[j+2]
        price = table.row_values(i)[j+3]
        platform_id = int(table.row_values(i)[j+4])
        if Room.objects.filter(Q(hotel_name=hotel_name) & Q(platform_id=platform_id) & Q(type=type)):
            room = Room.objects.get(Q(hotel_name=hotel_name) & Q(platform_id=platform_id) & Q(type=type))
            room.price = price
            if price == '0':
                room.count = 0
            else:
                room.count = random.randint(1, 10)
            room.save()
        else:
            if price == '0':
                Room.objects.create(hotel_name=hotel_name, type=type, price=price, platform_id=platform_id, count=0)
            else:
                Room.objects.create(hotel_name=hotel_name, type=type, price=price, platform_id=platform_id, count=random.randint(1, 10))

    data = {'status': 200, 'msg': 'success'}
    resp = JsonResponse(dict(data))
    return resp

## finish
def hotels(request):
    user_id = 1
    if not Booking.objects.filter(user_id=user_id).exists():
        hotels = list(Hotel.objects.filter(picture__startswith='http').order_by("-score")[0:50])
        data = [hotels[0].to_dict(), hotels[1].to_dict(), hotels[2].to_dict(), hotels[3].to_dict(), hotels[4].to_dict()]
    else:
        type = Booking.objects.get(user_id=user_id).hotel.type
        price = Booking.objects.get(user_id=user_id).hotel.price
        hotel_list = list(Hotel.objects.filter(type=type))
        hotels_dic = {}
        for hotel in hotel_list:
            hotels_dic[hotel] = abs(hotel.price-price)
        hotels_dic.items()
        L = list(hotels_dic.items())
        L.sort(key=lambda x:x[1], reverse=False)
        L = L[:5]
        data = [L[0][0].to_dict(), L[1][0].to_dict(), L[2][0].to_dict(), L[3][0].to_dict(), L[4][0].to_dict()]
    data = {'status': 200, 'msg': 'success', "data": data}
    resp = JsonResponse(dict(data))
    return resp

## finish
def popular(request):
    hotels = list(Hotel.objects.filter(picture__startswith='http').order_by("-sales")[0:3])
    data = [hotels[0].to_dict(), hotels[1].to_dict(), hotels[2].to_dict()]
    data = {'status': 200, 'msg': 'success', "data": data}
    resp = JsonResponse(dict(data))
    return resp

## finish
def rankAll(request):
    hotels = list(Hotel.objects.filter(price__gt=0).order_by("price")[0:10])
    listByPrice = [{'hotelName': hotel.name, 'price' : hotel.price} for hotel in hotels]

    hotels = list(Hotel.objects.order_by("-score")[0:10])
    listByScore = [{'hotelName': hotel.name, 'score' : hotel.score} for hotel in hotels]

    hotels = list(Hotel.objects.order_by("-sales")[0:10])
    listByPop = [{'hotelName': hotel.name, 'popValue' : hotel.sales} for hotel in hotels]

    data = {
        'tableDataByPrice': listByPrice,
        'tableDataByCom': listByScore,
        'tableDataByPop': listByPop,
    }
    data = {'status': 200, 'msg': 'success', "data": data}
    resp = JsonResponse(dict(data))
    return resp

## finish
def get_all_collections(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    user_id = body_dict.get('userid')
    collections = list(Collections.objects.filter(user_id=user_id))
    hotels = [collection.hotel for collection in collections]
    data = []
    for x in hotels:
        dic = x.to_dict()
        dic.pop('url')
        dic['time'] = Collections.objects.get(Q(user_id=user_id) & Q(hotel_id=x.id)).time
        data.append(dic)
    data = {'code': 200, 'msg': 'success', "data": data}
    resp = JsonResponse(dict(data))
    return resp

## finish
def addCollection(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    hotel_id = body_dict.get('hotel')
    user_id = body_dict.get('userid')
    time = body_dict.get('time')
    if Collections.objects.filter(Q(hotel_id=hotel_id) & Q(user_id=user_id)).exists():
        data = {'code': 200, 'msg': '加入收藏夹成功'}
    else:
        Collections.objects.create(hotel_id=hotel_id, user_id=user_id, time=time)
        data = {'code': 200, 'msg': '加入收藏夹成功'}
    resp = JsonResponse(dict(data))
    return resp

## finish
def addHistory(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    hotel_id = body_dict.get('hotel_id')
    user_id = body_dict.get('userid')
    time = body_dict.get('time')
    if History.objects.filter(Q(user_id=user_id) & Q(hotel_id=hotel_id)).exists():
        history = History.objects.get(Q(user_id=user_id) & Q(hotel_id=hotel_id))
        history.date = time
        history.save()
    else:
        History.objects.create(user_id=user_id, hotel_id=hotel_id, date=time)
    ## 人气值 +1
    hotel = Hotel.objects.get(id=hotel_id)
    hotel.popularity = hotel.popularity + 1
    hotel.save()
    data = {'status': 200, 'msg': 'success'}
    resp = JsonResponse(dict(data))
    return resp


def delete(request):
    b = User.objects.filter(id=2).first()
    b.delete()
    # while Hotel.objects.exists():
    #     hotel = Hotel.objects.first()
    #     hotel.delete()
    # while HotelDetail.objects.exists():
    #      hotel = HotelDetail.objects.first()
    #      hotel.delete()
    # while Hotel.objects.exists():
    #      hotel = Hotel.objects.first()
    #      hotel.delete()
    data = {'status': 200, 'msg': 'success'}
    resp = JsonResponse(dict(data))
    return resp

## TODO
def regress(price_list, date_list):
    pl = [price_list[0]]
    dl = [date_list[0]]
    price_base = mean(price_list)
    rg_datelist = ['2021-12-12', '2021-12-14', '2021-12-16']
    for x in rg_datelist:
        pl.append(price_base + random.randint(int(-price_base/5), int(price_base/5)))
        dl.append(x)
    pl.append(price_list[1])
    dl.append(date_list[1])
    rg_datelist = ['2021-12-18', '2021-12-20', '2021-12-22', '2021-12-24']
    for x in rg_datelist:
        pl.append(price_base + random.randint(int(-price_base/5), int(price_base/5)))
        dl.append(x)
    pl.append(price_list[2])
    dl.append(date_list[2])
    return [pl, dl]


def to_price_dict(price, date):
    dic = {
        'date': date,
        'price': price,
    }
    return dic

## TODO
def price(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    #print(body_dict)
    hotel_id = body_dict.get('hotel_id')
    name = Hotel.objects.get(id=hotel_id).name
    platform = Hotel.objects.get(id=hotel_id).platform_id
    details = list(HotelDetail.objects.filter(Q(name=name) & Q(platform_id=platform)))

    dates = [detail.date for detail in details]
    price_list = [detail.price for detail in details]
    score_list = [detail.score for detail in details]
    sales_list = [detail.sales for detail in details]

    tmp = regress(price_list, dates)
    price_data = [to_price_dict(tmp[0][i], tmp[1][i]) for i in range(len(tmp[0]))]
    # price_data = [to_price_dict(price_list[i], dates[i]) for i in range(len(dates))]
    data = {'status': 200, 'data': price_data}
    resp = JsonResponse(dict(data))
    return resp

## finish
def addLeaveMessage(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    user_id = body_dict.get('userid')
    hotel_id = body_dict.get('comid')
    date = body_dict.get('time')
    context = body_dict.get('message')
    Comment.objects.create(user_id=user_id, hotel_id=hotel_id, date=date, context=context)
    data = {'status': 200, 'msg': '成功'}
    resp = JsonResponse(dict(data))
    return resp

## finish
def addReplyMessage(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    user_id = body_dict.get('userid')
    context = body_dict.get('message')
    comment_id = body_dict.get('leavemessageid')
    date = body_dict.get('time')
    Comment_Reply.objects.create(user_id=user_id, comment_id=comment_id, context=context, date=date)
    data = {'status': 200, 'msg': 'success'}
    resp = JsonResponse(dict(data))
    return resp

## finish
def leavemessage(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    hotel_id = body_dict.get('hotel_id')
    messages = list(Comment.objects.filter(hotel_id=hotel_id))
    msgdata = [msg.to_dict() for msg in messages]
    data = {'status': 200, 'data': msgdata}
    resp = JsonResponse(dict(data))
    return resp

## finish
def replymessage(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    message_id = body_dict.get('leaveMessage_id')
    replys = list(Comment_Reply.objects.filter(comment_id=message_id))
    replydata = [reply.to_dict() for reply in replys]
    data = {'status' : 200, 'data' : replydata}
    resp = JsonResponse(dict(data))
    return resp

## finish
def getAllHistory(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    user_id = body_dict.get('userid')
    historys = list(History.objects.filter(user_id=user_id))
    hotels = [history.hotel for history in historys]
    data = []
    for x in hotels:
        dic = x.to_dict()
        dic['time'] = History.objects.get(Q(user_id=user_id) & Q(hotel_id=x.id)).date
        data.append(dic)
    data = {'code': 200, 'data': data} # the time when user last open this hotel
    resp = JsonResponse(dict(data))
    return resp

## TODO
def delHistory(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    #print(body_dict)
    # user_id = 1
    # hotel_id = 656
    # history = History.objects.get(Q(user_id=user_id) & Q(hotel_id=hotel_id))
    # history.delete()
    data = {'code':200, 'msg': '删除成功'}
    resp = JsonResponse(dict(data))
    return resp

## finish
def delAllHistories(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    user_id = body_dict.get('userid')
    while History.objects.filter(user_id=user_id).exists():
        history = History.objects.filter(user_id=user_id).first()
        history.delete()
    data = {'code':200, 'msg': '删除成功'}
    resp = JsonResponse(dict(data))
    return resp

## TODO
def delCollection(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    #print(body_dict)
    # user_id = 1
    # hotel_id = 656
    # collection = Collections.objects.get(Q(user_id=user_id) & Q(hotel_id=hotel_id))
    # collection.delete()
    data = {'code':200, 'msg': '删除成功'}
    resp = JsonResponse(dict(data))
    return resp

## finish
def delAllCollections(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    user_id = body_dict.get('userid')
    while Collections.objects.filter(user_id=user_id).exists():
        collection = Collections.objects.filter(user_id=user_id).first()
        collection.delete()
    data = {'code':200, 'msg': '删除成功'}
    resp = JsonResponse(dict(data))
    return resp

## TODO
def updateLocHotel(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    data = {'code': 200, 'msg': '修改酒店信息成功'}
    resp = JsonResponse(dict(data))
    return resp


def min_edit(s, t):
    n = len(s)
    m = len(t)
    D = np.zeros((n+1, m+1))
    for i in range(n + 1):
        D[i][0] = i
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            c = 0
            if s[i-1] != t[j-1]:
                c = 1
            replace = D[i-1][j-1] + c
            delete = D[i-1][j] + 1
            insert = D[i][j-1] + 1
            if replace == min(replace, delete, insert):
                D[i][j] = D[i-1][j-1] + c
            elif insert == min(replace, delete, insert):
                D[i][j] = D[i, j-1] + 1
            else:
                D[i][j] = D[i-1][j] + 1
    return D[n][m]


def booking(request):
    user_id = 1
    hotel_id = 7
    date = '2021-12-29'
    Booking.objects.create(user_id=user_id, hotel_id=hotel_id, date=date)
    data = {'code': 200, 'msg': '修改酒店信息成功'}
    resp = JsonResponse(dict(data))
    return resp

## TODO
def searchHotel(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    search_name = body_dict["keyword"]
    if Hotel.objects.filter(name__icontains=search_name).exists():
        hotel_list = list(Hotel.objects.filter(name__icontains=search_name))[:10]
        res = [hotel.name for hotel in hotel_list]
    else:
        hotel_list = list(Hotel.objects.all())
        hotels_dic = {}
        for hotel in hotel_list:
            hotels_dic[hotel] = min_edit(hotel.name, search_name)
        hotels_dic.items()
        L = list(hotels_dic.items())
        L.sort(key=lambda x:x[1], reverse=False)
        L = L[:10]
        res = [ele[0].name for ele in L]
    print(res)
    data = {'code': 200, 'msg': '修改酒店信息成功'}
    resp = JsonResponse(dict(data))
    return resp

## finish
def addScore(request):
    body_json = request.body.decode()
    print(body_json)
    body_dict = json.loads(body_json)
    print(body_dict)
    hotel_id = body_dict.get('hotel_id')
    user_id = body_dict.get('userid')
    score = body_dict.get('score')
    time = body_dict.get('time')
    hotel = Hotel.objects.get(id=hotel_id)
    hotel.score = (hotel.score * hotel.score_count + score) / (hotel.score_count + 1)
    hotel.score_count = hotel.score_count + 1
    hotel.save()
    data = {'code': 200, 'msg': '打分成功'}
    resp = JsonResponse(dict(data))
    return resp

## TODO
def update_logo(request):
    img = request.FILES.get('img') # 新的log
    print(img)
    data = {'code': 200, 'msg': '更新logo成功', 'img_src':'http:xxx'}
    resp = JsonResponse(dict(data))
    return resp


def map_update(request):
    body_json = request.body.decode()
    print(body_json)
    body_dict = json.loads(body_json)
    print(body_dict)
    data = {'code': 200, 'msg': '更新成功'}
    resp = JsonResponse(dict(data))
    return resp

def queryRoomInfo(request):
    body_json = request.body.decode()
    print(body_json)
    body_dict = json.loads(body_json)
    print(body_dict)
    data = {'code': 200, 'roomInfo': [
        { "id": 1, "type": "单人房", "price": "120", 'remain': 2 },
        { "id": 2, "type": "双人房", "price": "180", 'remain': 4 },
      ]}
    resp = JsonResponse(dict(data))
    return resp


def book(request):
    body_json = request.body.decode()
    print(body_json)
    body_dict = json.loads(body_json)
    print(body_dict)
    data = {'code': 200, 'msg': '房间预订成功'}
    resp = JsonResponse(dict(data))
    return resp

# def login(request):
#     body_json = request.body.decode()
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     mail = body_dict.get('mail')
#     password = body_dict.get('password')
#     userInfo = None
#     code = 0
#     if not User.objects.filter(email=mail):
#         code = 404
#         msg = "用户不存在"
#     else:
#         user = User.objects.get(email=mail)
#         if user.password == password:
#             code = 200
#             msg = "登陆成功"
#             userInfo = user.to_dict()
#             print(userInfo)
#             userInfo['type'] = 2
#             userInfo['loc_hotel'] = {'comname': 'a',
#                                  'comid': userInfo['id'],
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/daoqi.jpg',
#              'platform': 'local',
#              'favorrate': 0.92,
#              'sales': 123,
#              'newestprice': 120,
#              'name': '北京万达文华酒店',
#              'address': '北京朝阳区建国路93号万达广场C座',
#              'cid': 1,
#              'room': [{'id': 1, 'type': '单人间', '总量': 150, '已预约': 55, 'price': 123}, {'id': 2, 'type':'双人间', '总量': 150, '已预约': 131, 'price': 133}],
#              'roomInfo': {'single': {'amount': 150, 'subscribed': 45, 'price': 123},
#                           'double': {'amount': 150, 'subscribed': 131, 'price': 133},
#                           'triple': None},
#              'regTime': '2021-12-3',
#         }
#         else:
#             code = 402
#             msg = "密码错误"
#     data = {'code': code, 'msg': msg, "userInfo": userInfo}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def hotels(request):
#     data = [{'comnae': 'test',
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/daoqi.jpg',
#              'platform': 'local',
#              'favorrate': 0.92,
#              'sales': 123,
#              'newestprice': 120,
#              'name': '北京哈哈哈酒店',
#              'address': '海淀区学院路31号',
#              'cid': 1,
#              'url': "https://hotel.elong.com/hotel/hoteldetail?hotelId=40101927&inDate=2021-12-27&outDate=2021-12-28",
#              'room': [{'id': 1, 'type': '单人间', '总量': 150, '已预约': 55, 'price': 123},
#                       {'id': 2, 'type': '双人间', '总量': 150, '已预约': 131, 'price': 133}],
#              'roomInfo': {'single': {'amount': 150, 'subscribed': 45, 'price': 123},
#                           'double': {'amount': 150, 'subscribed': 131, 'price': 133},
#                           'triple': None},
#              },
#             {'comnae': 'test',
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/liyue.jpg',
#              'platform': 'platform',
#              'favorrate': 0.98,
#              'sales': 123,
#              'newestprice': 100,
#              'name': '北京哈酒店',
#              'address': '海淀区学院路31号',
#              'cid': 2,
#              'url': "https://hotel.elong.com/hotel/hoteldetail?hotelId=40101927&inDate=2021-12-27&outDate=2021-12-28"},
#             {'comnae': 'test',
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/mengde.jpg',
#              'platform': 'platform',
#              'favorrate': 0.40,
#              'sales': 123,
#              'newestprice': 198,
#              'name': '北京哈哈酒店',
#              'address': '海淀区学院路31号',
#              'cid': 3,
#              'url': "https://hotel.elong.com/hotel/hoteldetail?hotelId=40101927&inDate=2021-12-27&outDate=2021-12-28"}
#             ]
#     data = {'status': 200, 'msg': 'success', "data": data}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def popular(request):
#     data = [{'comnae': 'test',
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/daoqi.jpg',
#              'platform': 'platform',
#              'favorrate': 0.92,
#              'sales': 123,
#              'newestprice': 100,
#              'name': '北京哈哈哈酒店',
#              'cid': 1,
#              'address': '海淀区学院路31号',
#              'url': "https://hotel.elong.com/hotel/hoteldetail?hotelId=40101927&inDate=2021-12-27&outDate=2021-12-28"},
#
#             {'comnae': 'test',
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/liyue.jpg',
#              'platform': 'platform',
#              'favorrate': 0.98,
#              'sales': 123,
#              'newestprice': 100,
#              'name': '北京哈酒店',
#              'cid': 2,
#              'address': '海淀区学院路31号',
#              'url': "https://hotel.elong.com/hotel/hoteldetail?hotelId=40101927&inDate=2021-12-27&outDate=2021-12-28"},
#
#             {'comnae': 'test',
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/mengde.jpg',
#              'platform': 'platform',
#              'favorrate': 0.40,
#              'sales': 123,
#              'newestprice': 128,
#              'name': '北京哈哈酒店',
#              'cid': 3,
#              'address': '海淀区学院路31号',
#              'url': "https://hotel.elong.com/hotel/hoteldetail?hotelId=40101927&inDate=2021-12-27&outDate=2021-12-28"}
#             ]
#     data = {'status': 200, 'msg': 'success', "data": data}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def get_all_collections(request):
#     data = [{'comnae': 'test',
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/daoqi.jpg',
#              'platform': 'platform',
#              'favorrate': 0.92,
#              'sales': 123,
#              'newestprice': 100,
#              'address': '海淀区学院路31号',
#              'name': '北京哈哈哈酒店',
#              'cid': 1,
#              'time': "2021-12-28"}, # the time when user star this hotel
#
#             {'comnae': 'test',
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/liyue.jpg',
#              'platform': 'platform',
#              'favorrate': 0.98,
#              'sales': 123,
#              'newestprice': 100,
#              'name': '北京哈酒店',
#              'address': '海淀区学院路31号',
#              'cid': 2},
#
#             {'comnae': 'test',
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/mengde.jpg',
#              'platform': 'platform',
#              'favorrate': 0.40,
#              'sales': 123,
#              'newestprice': 128,
#              'name': '北京哈哈酒店',
#              'address': '海淀区学院路31号',
#              'cid': 3}
#             ]
#     data = {'code': 200, 'msg': 'success', "data": data}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def rankAll(request):
#     data = {
#         'tableDataByPrice': [
#             {'hotelName': "北京哈哈哈酒店", 'price': 198},
#             {'hotelName': "北京哈哈酒店", 'price': 199},
#             {'hotelName': "北京哈酒店", 'price': 200},
#         ],
#
#         'tableDataByCom': [
#             {'hotelName': "北京哈哈哈酒店", 'score': 0.99},
#             {'hotelName': "北京哈哈酒店", 'score': 0.98},
#             {'hotelName': "北京哈酒店", 'score': 0.97},
#         ],
#
#         'tableDataByPop': [
#             {'hotelName': "北京哈哈哈酒店", 'popValue': 99},
#             {'hotelName': "北京哈哈酒店", 'popValue': 98},
#             {'hotelName': "北京哈酒店", 'popValue': 97},
#         ],
#
#     }
#     data = {'status': 200, 'msg': 'success', "data": data}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def addHistory(request):
#     print(request.body)
#     data = {'status': 200, 'msg': 'success'}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def price(request):
#     body_json = request.body.decode()
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'status': 200, 'data': [ {'date': '2021-12-12', 'price': 656.0}, {'date': '2021-12-14', 'price': 585.0}, {'date': '2021-12-16', 'price': 811.0}, {'date': '2021-12-18', 'price': 827.0}, {'date': '2021-12-20', 'price': 672.0}, {'date': '2021-12-22', 'price': 851.0}, {'date': '2021-12-24', 'price': 767.0}]}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def leavemessage(request):
#     body_json = request.body.decode()
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'status': 200, 'data': [{'id': 1, 'userid': 1, 'time': "2020-11-7", 'hotel_id': 1, 'message': '北航校内的酒店嘛~ 牛b'},
#                                     {'id': 2, 'userid': 1, 'time': "2020-11-8", 'hotel_id': 1, 'message': '为啥我的评论没有回复啊!?'}]}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def replymessage(request):
#     body_json = request.body.decode()
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     list = [{'id': 1, 'userid': 1, 'time': "2020-11-7", 'leavemessageid': 1, 'message': '这是一条评论'},
#                      {'id': 2, 'userid': 1, 'time': "2020-11-8", 'leavemessageid': 1, 'message': '这是另一条评论'}] if body_dict['leaveMessage_id'] == 1 else []
#     data = {'status': 200,
#             'data': list}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def user(request):
#     print(request)
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code': 200,
#             'msg': '注册成功'}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def getAllHistory(request):
#     data = {'code': 200, 'data': [{
#              'piclink': 'http://sun-zeyi.gitee.io/cnblog/pictures/mengde.jpg',
#              'platform': '艺龙',
#              'newestprice': 128,
#              'name': '北京哈哈酒店',
#              'cid': 3, 'time': "2021-12-28"}]} # the time when user last open this hotel
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def delAllHistories(request):
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code':200, 'msg': '删除成功'}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def delAllCollections(request):
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code': 200, 'msg': '删除成功'}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def updateUser(request):
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code': 200, 'msg': '修改用户信息成功'}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def updateLocHotel(request):
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code': 200, 'msg': '修改酒店信息成功'}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def addLeaveMessage(request):
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code': 200, 'msg': '添加留言成功'}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def addReplyMessage(request):
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code': 200, 'msg': '添加回复成功'}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def addScore(request):
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code': 200, 'msg': '打分成功'}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def addCollection(request):
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code': 200, 'msg': '加入收藏夹成功'}
#     resp = JsonResponse(dict(data))
#     return resp
#
#

def upload(img):
    headers = {'Authorization': 'cMZkqPKLXfroLwwGBqpYtunwkKm6BvUp'}
    files = {'smfile': img}
    url = 'https://sm.ms/api/v2/upload'
    res = requests.post(url, files=files, headers=headers, verify=False).json()
    print(json.dumps(res, indent=4))


def update_logo(request):
    img = request.FILES.get('img') # 新的log
    upload(img)
    data = {'code': 200, 'msg': '更新logo成功', 'img_src':'http:xxx'}
    resp = JsonResponse(dict(data))
    return resp
#
#
def map_update(request):
    body_json = request.body.decode()
    print(body_json)
    body_dict = json.loads(body_json)
    print(body_dict)
    data = {'code': 200, 'msg': '更新成功'}
    resp = JsonResponse(dict(data))
    return resp
#
#
# def queryRoomInfo(request):
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code': 200, 'roomInfo': [
#         { "id": 1, "type": "单人房", "price": "120", 'remain': 2 },
#         { "id": 2, "type": "双人房", "price": "180", 'remain': 4 },
#       ]}
#     resp = JsonResponse(dict(data))
#     return resp
#
#
# def book(request):
#     body_json = request.body.decode()
#     print(body_json)
#     body_dict = json.loads(body_json)
#     print(body_dict)
#     data = {'code': 200, 'msg': '房间预订成功'}
#     resp = JsonResponse(dict(data))
#     return resp