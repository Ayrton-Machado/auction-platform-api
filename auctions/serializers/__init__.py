"""
Views da aplicação Auctions.
Organizadas por domínio.
"""

from .auctions import AuctionSerializer, CreateListingSerializer
from .auth import LoginSerializer, RegisterSerializer
from .bids import BidSerializer, PlaceBidSerializer
from .comments import CommentsSerializer, AddCommentSerializer
from .watchlist import WatchlistSerializer, WatchlistAddAuctionSerializer
from .categories import CategorySerializer

__all__ = [
    # Authentication
    'LoginSerializer',
    'RegisterSerializer',
    
    # Auctions
    'AuctionSerializer',
    'CreateListingSerializer',
    
    # Bids
    'BidSerializer',
    'PlaceBidSerializer',
    
    # Comments
    'AddCommentSerializer',
    'CommentsSerializer',
    
    # Watchlist
    'WatchlistAddAuctionSerializer',
    'WatchlistSerializer',
    
    # Categories
    'CategorySerializer'
]
