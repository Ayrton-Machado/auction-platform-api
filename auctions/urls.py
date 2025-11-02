from django.urls import path

from . import views

urlpatterns = [
    path("auctions/", views.indexAPI.as_view(), name="api-auctions"),

    # Auth endpoints
    path("login", views.LoginAPI.as_view(), name="api-login"),
    path("logout", views.LogoutAPI.as_view(), name="api-logout"),
    path("register", views.RegisterAPI.as_view(), name="api-register"),

    # Core auction endpoints
    path('create_listing/', views.CreateListingAPI.as_view(), name='api-createListing'),
    path('listing/<int:listing_id>', views.ListingPageAPI.as_view(), name='api-pageListing'),
    path('listing/<int:listing_id>/bid', views.PlaceBidAPI.as_view(), name='api-placeBid'),
    path('listing/<int:listing_id>/close', views.CloseAuctionAPI.as_view(), name='api-closeAuction'),
    path('listing/<int:listing_id>/comment', views.AddCommentAPI.as_view(), name='api-addComment'),
    path('watchlist/', views.WatchlistAuctionAPI.as_view(), name='api-watchlistAuction'),
    path('watchlist/<int:listing_id>/add', views.WatchlistAddAuctionAPI.as_view(), name='api-watchlistAddAuction'),
    path('watchlist/remove', views.WatchlistRemoveAPI.as_view(), name='api-watchlistRemove'),
    path('categories/', views.ShowCategoriesAPI.as_view(), name='api-showCategories'),
    path('categories/<int:selectedCategory>', views.CategoriesAuctionsAPI.as_view(), name='api-categoryAuctions')
]
