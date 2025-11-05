"""
Views da aplicação Auctions.
Organizadas por domínio.
"""

from .auth import LoginAPI, RegisterAPI, LogoutAPI
from .auctions import CreateListingAPI, indexAPI, ListingPageAPI, CloseAuctionAPI, CategoriesAuctionsAPI
from .bids import PlaceBidAPI
from .categories import ShowCategoriesAPI
from .comments import AddCommentAPI
from .watchlist import WatchlistRemoveAPI, WatchlistAuctionAPI, WatchlistAddAuctionAPI

__all__ = [
    # Authentication
    'LoginAPI',
    'RegisterAPI',
    'LogoutAPI',
    
    # Auctions
    'indexAPI',
    'CreateListingAPI',
    'ListingPageAPI',
    'CloseAuctionAPI',
    
    # Bids
    'PlaceBidAPI',
    
    # Comments
    'AddCommentAPI',
    
    # Watchlist
    'WatchlistAddAuctionAPI',
    'WatchlistAuctionAPI',
    'WatchlistRemoveAPI',
    
    # Categories
    'ShowCategoriesAPI',
    'CategoriesAuctionsAPI',
]