from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import authenticate, login, logout

class User(AbstractUser):
    pass

class Category(models.Model):
    categories = models.CharField(max_length=64, blank=True, unique=True)

    def __str__(self):
        return f'{self.categories}'

class AuctionListing(models.Model):
    title = models.CharField(max_length=64, blank=True)
    description = models.TextField(max_length=500, blank=True)
    bidstart = models.IntegerField(blank=True)
    urlImage = models.CharField(max_length=500, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, max_length=64, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=64, blank=True, unique=True)

    def __str__(self):
        return f'ID: {self.id} Título: {self.title}\nDescrição: {self.description}\nBID: {self.bidstart}\n CATG: {self.category}\n URL: {self.urlImage}\n Created by: {self.createdBy}'

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass

