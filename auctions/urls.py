from django.urls import path

from . import views

urlpatterns = [
    path("api/auctions", views.indexAPI.as_view(), name="api-auctions"),

    path("api/login", views.LoginAPI.as_view(), name="api-login"),
    path("api/logout", views.LogoutAPI.as_view(), name="api-logout"),
    path("api/register", views.RegisterAPI.as_view(), name="api-register"),

    path('api/create_listing', views.CreateListingAPI.as_view(), name='api-createListing'),
    path('api/listing/<str:listing_id>', views.listing, name='listing'),
    path('api/listing/<str:listing_id>/bid', views.placeBid, name='placebid'),
    path('api/listing/<str:listing_id>/close', views.closeAuction, name='closeAuction'),
    path('api/listing/<str:listing_id>/comment', views.addComment, name='addComment'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('watchlist/remove', views.watchlistRemove, name='watchlistRemove'),
    path('categories', views.Categories, name='categories'),
    path('categories/<str:which_category>', views.whichCategory, name='category'),
    path('error', views.error, name='error')
]
