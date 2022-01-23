from django.contrib import admin
from backdb.models import *
# Register your models here.
admin.site.register([User, Booking, Business, Collections, Comment, Comment_Reply,
                     History, Hotel, HotelDetail, Platform, PopularRank, PriceRank, ScoreRank,
                     Room])