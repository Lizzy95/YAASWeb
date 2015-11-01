from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import datetime
from django.utils import timezone

class Auction(models.Model):
    idItem = models.AutoField(primary_key=True)
    titleAuc =models.CharField(max_length=50)
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    deadLine = models.DateTimeField(db_index=True)
    content = models.TextField()
    minPrice = models.FloatField(default=0.0)
    locked = models.TextField(default="")
    author = models.TextField(default="")
    authoremail = models.TextField(default="")
    bidder = models.TextField(default="")
    bidderemail = models.TextField(default="")
    banded = models.TextField(default="")
    resolve = models.TextField(default="")

    def __str__(self):
        return self.titleAuc

    @classmethod
    def getByidItem(cls, idItem):
        return cls.objects.get(idItem=idItem)

    @classmethod
    def exists(cls, idItem):
        return len(cls.objects.filter(idItem=idItem)) > 0

    @classmethod
    def getBytitleAuc(cls, titleAuc):
        return cls.objects.get(titleAuc=titleAuc)

class Bidders(models.Model):
    bidderName = models.TextField(default="")
    bidderEmail = models.TextField(default="")
    bidItem = models.IntegerField(default="")

    @classmethod
    def getBybidItem(cls, bidItem):
        return cls.objects.get(bidItem=bidItem)

