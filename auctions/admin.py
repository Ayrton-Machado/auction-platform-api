from django.contrib import admin
from .models import Category, User, AuctionListing, Comments, Bids, Watchlist
# Register your models here.

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'bidstart', 'category', 'createdBy', 'closed')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'comment')

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'item')

admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Bids)
admin.site.register(Watchlist, WatchlistAdmin)