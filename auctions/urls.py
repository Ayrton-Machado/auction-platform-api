from django.urls import path

from . import views

urlpatterns = [
    path("api/auctions", views.indexAPI.as_view(), name="api-auctions"),
    path("api/login", views.LoginAPI.as_view(), name="api-login"),
    path("api/logout", views.logout_view, name="logout"),
    path("api/register", views.register, name="register"),
    path('api/createlisting', views.create_listing, name='createlisting'),
    path('api/listing/<str:listing_id>', views.listing, name='listing'),
    path('api/listing/<str:listing_id>/bid', views.placeBid, name='placebid'),
    path('api/listing/<str:listing_id>/close', views.closeAuction, name='closeAuction'),
    path('api/listing/<str:listing_id>/comment', views.addComment, name='addComment'),
    path('api/watchlist', views.watchlist, name='watchlist'),
    path('api/watchlist/remove', views.watchlistRemove, name='watchlistRemove'),
    path('api/categories', views.Categories, name='categories'),
    path('api/categories/<str:which_category>', views.whichCategory, name='category'),
    path('api/error', views.error, name='error')
]
