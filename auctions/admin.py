from django.contrib import admin
from .models import Category, User, AuctionListing, Comments, Bids, Watchlist
# Register your models here.

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Bids)
 
@admin.register(AuctionListing)
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'starting_bid', 'category', 'created_by', 'closed', 'winner')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'comment', 'created_at')

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')