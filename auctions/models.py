from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone 

class User(AbstractUser):
    email = models.EmailField(blank=False)

    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_reason = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower('username'),
                name='unique_username_ci'
            ),
            models.UniqueConstraint(
                models.functions.Lower('email'),
                name='unique_email_ci'
            )
        ]

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return f'ID: {self.id} name: {self.name}'

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500, blank=True, default='')
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=500, blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions_created')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='auctions')
    closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='auctions_won')
    winning_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.title} (${self.starting_bid})'
    
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Bids"
        ordering = ["-amount"]

    def __str__(self):
        return f'{self.user.username}: ${self.amount} on {self.listing.title}'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='watchers')

    class Meta:
        unique_together = ['user', 'listing']  # Impede duplicidade

    def __str__(self):
        return f'{self.id} {self.user} : {self.listing}'

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.user.username} on {self.listing.title}'

