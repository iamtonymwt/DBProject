from django.urls import path, include
from rest_framework.routers import DefaultRouter

from backdb import views
from backdb.views import login
from backdb.views import hotels
from backdb.views import popular
from backdb.views import get_all_collections
from backdb.views import rankAll
from backdb.views import addHistory
from backdb.views import price
from backdb.views import leavemessage
from backdb.views import *
from django.contrib import admin

#router = DefaultRouter()
#router.register('user', views.UserViewSet)

urlpatterns = [
    path('Login/', login),
    path('hotels/', hotels),
    path('popular/', popular),
    path('getAllCollections/', get_all_collections),
    path('rankAll/', rankAll),
    path('addHistory/', addHistory),
    path('price/', price),
    path('leavemessage/', leavemessage),
    path('replymessage/', replymessage),
    path('user/', user),
    path('getAllHistories/', getAllHistory),
    path('delAllHistories/', delAllHistories),
    path('delAllCollections/', delAllCollections),
    path('updateUser/', updateUser),
    path('updateLocHotel/', updateLocHotel),
    path('addLeaveMessage/', addLeaveMessage),
    path('addReplyMessage/', addReplyMessage),
    path('addScore/', addScore),
    path('addCollection/', addCollection),
    path('upload_logo/', update_logo),
    path('MapUpdate/', map_update),
    path('queryRoomInfo/', queryRoomInfo),
    path('book/', book),
    path('delHistory/', delHistory),
    path('delCollection/', delCollection),
    path('delete/', delete),
    path('loadExcel/', loadExcel),
    path('tt/', searchHotel),
    path('admin/', admin.site.urls),
    path('searchHotel/', searchHotel)
]