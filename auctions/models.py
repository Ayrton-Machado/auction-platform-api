from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import authenticate, login, logout

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=200)
    bidstart = models.IntegerField()
    urlImage = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.title}\n{self.description}\n{self.bidstart}'

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass

class User(AbstractUser):
    pass
