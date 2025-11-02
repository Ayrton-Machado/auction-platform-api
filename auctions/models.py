from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import authenticate, login, logout

class User(AbstractUser):
    pass

class Category(models.Model):
    categories = models.CharField(max_length=64, blank=True, unique=True)

    def __str__(self):
        return f'ID: {self.id} Categories: {self.categories}'


class AuctionListing(models.Model):
    title = models.CharField(max_length=64, blank=True)
    description = models.TextField(max_length=500, blank=True)
    bidstart = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    urlImage = models.CharField(max_length=500, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, max_length=64, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, max_length=64, blank=True, null=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f'ID: {self.id} Título: {self.title} | BID: {self.bidstart} | CATG: {self.category} | Created by: {self.createdBy} | Closed: {self.closed} |'

class Bids(models.Model):
    bidUser = models.ForeignKey(User, on_delete=models.CASCADE, max_length=64, blank=True)
    bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bidItem = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return f'{self.bidUser} : {self.bid}'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'{self.id} {self.user} : {self.item}'

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.user}\n{self.comment}'

