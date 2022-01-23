from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=32)
    date = models.DateField(default='2021-12-29')
    rank = models.IntegerField(default=1)

    def to_dict(self):
        return {'id': self.id, 'username': self.name, 'email': self.email, 'password': self.password, 'date': self.date}


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=32)
    rank = models.IntegerField(default=1)

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    email = models.EmailField()
    date = models.DateField(default='2021-12-29')
    password = models.CharField(max_length=32)
    rank = models.IntegerField(default=1)
    def to_dict(self):
        return {'id': self.id, 'username': self.name, 'email': self.email, 'password': self.password, 'date': self.date}

class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey("Business", default=1, on_delete=models.CASCADE)
    platform = models.ForeignKey("Platform", default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    picture = models.CharField(max_length=256, blank=True, null=True)
    type = models.CharField(max_length=32, default="经济型")
    sales = models.IntegerField(default=100)
    score_count = models.IntegerField(default=50)
    price = models.IntegerField(default=100)
    popularity = models.IntegerField(default=6666)
    #score = models.DecimalField(max_digits=8, decimal_places=8, default=0)
    score = models.DecimalField(max_digits=4, decimal_places=2, default=5.0)
    longlatitude = models.CharField(max_length=64, default="0.0, 0.0")
    url = models.CharField(max_length=256, blank=True)
    #longitude = models.DecimalField(max_digits=8, decimal_places=8)
    #latitude = models.DecimalField(max_digits=8, decimal_places=8)
    def to_dict(self):
        comnae = Business.objects.get(id=self.business_id).name
        if self.picture.find("http") >= 0:
            piclink = self.picture
        else:
            piclink = "http://pic.lvmama.com/img/searchList/hotel/hotel_no_photo_list.png"
        platform = Platform.objects.get(id=self.platform_id).name
        favorrate = self.score
        sales = self.sales
        newestprice = self.price
        name = self.name
        cid = self.id
        address= self.address
        url = self.url
        dic = {
            'comnae': comnae,
            'piclink': piclink,
            'platform': platform,
            'favorrate': favorrate,
            'sales': sales,
            'newestprice': newestprice,
            'name': name,
            'cid': cid,
            'address': address,
            'url': url,
            'room': [{'id': 1, 'type': '单人间', '总量': 150, '已预约': 55, 'price': 123},
                     {'id': 2, 'type': '双人间', '总量': 150, '已预约': 131, 'price': 133}],
            'roomInfo': {'single': {'amount': 150, 'subscribed': 45, 'price': 123},
                         'double': {'amount': 150, 'subscribed': 131, 'price': 133},
                         'triple': None},
        }
        return dic

class HotelDetail(models.Model):
    name = models.CharField(max_length=32)
    platform = models.ForeignKey("Platform", default=1, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.IntegerField(default=100)
    sales = models.IntegerField(default=233)
    score = models.DecimalField(max_digits=4, decimal_places=2, default=5.0)

    def to_price_dict(self):
        dic = {
            'date': self.date,
            'price': self.price,
        }
        return dic

    def to_score_dict(self):
        dic = {
            'date': self.date,
            'favorrate': self.score,
        }
        return dic

    def to_sales_dict(self):
        dic = {
            'date': self.date,
            'popular': self.sales,
        }
        return dic

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    hotel_id = models.IntegerField(blank=True, null=True)
    hotel_name = models.CharField(max_length=32)
    platform = models.ForeignKey("Platform", default=1, on_delete=models.CASCADE)
    type = models.CharField(max_length=32)
    price = models.IntegerField(default=100)
    count = models.IntegerField(default=3)
    sum = models.IntegerField(default=50)
    date = models.DateField(default='2021-12-29')

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE)
    date = models.CharField(max_length=32, default='2021-12-29')
    context = models.CharField(max_length=500)

    def to_dict(self):
        dic = {
            'id' : self.id,
            'userid' : self.user_id,
            'time' : self.date,
            'hotel_id' : self.hotel_id,
            'message' : self.context,
        }
        return dic

class Comment_Reply(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)        # on_delete
    date = models.CharField(max_length=32, default='2021-12-29')
    context = models.CharField(max_length=500)
    def to_dict(self):
        dic = {
            'id' : self.id,
            'userid' : self.user_id,
            'time' : self.date,
            'leavemessageid' : self.comment_id,
            'message' : self.context
        }
        return dic

class History(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE)
    date = models.CharField(max_length=32, default='2021-12-29')

class Collections(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    time = models.CharField(max_length=32, default='2021-12-29')

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE)
    date = models.CharField(max_length=32, default='2021-12-29')

class PopularRank(models.Model):
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE)
    rank = models.IntegerField(default=1)

class ScoreRank(models.Model):
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE)
    rank = models.IntegerField(default=1)

class PriceRank(models.Model):
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE)
    rank = models.IntegerField(default=1)