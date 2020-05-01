from django.db import models


class Product(models.Model):
    name = models.CharField(max_length= 255)
    price = models.FloatField()
    stock = models.IntegerField()
    nominal = models.CharField(max_length=10)
    image_url = models.CharField(max_length= 2083)


class Offer(models.Model):
    code = models.CharField(max_length= 10)
    description = models.CharField(max_length= 200)
    value = models.IntegerField()