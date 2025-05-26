from django.urls import path

from . import views

urlpatterns = [
    path("api/auctions/", views.indexAPI.as_view(), name="api-auctions"),

    path("api/login", views.LoginAPI.as_view(), name="api-login"),
    path("api/logout", views.LogoutAPI.as_view(), name="api-logout"),
    path("api/register", views.RegisterAPI.as_view(), name="api-register"),

    path('api/create_listing', views.CreateListingAPI.as_view(), name='api-createListing'),
    path('api/listing/<str:listing_id>', views.ListingPageAPI.as_view(), name='api-pageListing'),
    path('api/listing/<str:listing_id>/bid', views.PlaceBidAPI.as_view(), name='api-placeBid'),
    path('api/listing/<str:listing_id>/close', views.CloseAuctionAPI.as_view(), name='api-closeAuction'),
    path('api/listing/<str:listing_id>/comment', views.AddCommentAPI.as_view(), name='api-addComment'),
    path('api/watchlist', views.WatchlistAddAuctionAPI.as_view(), name='api-watchlistAddAuction'),
    path('api/watchlist/remove', views.WatchlistRemoveAPI.as_view(), name='api-watchlistRemove'),
    path('api/categories', views.ShowCategoriesAPI.as_view(), name='api-showCategories'),
    path('api/categories/<str:selectedCategory>', views.CategoriesAuctionsAPI.as_view(), name='api-categoryAuctions')
]
