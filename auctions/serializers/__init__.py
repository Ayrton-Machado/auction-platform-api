"""
Views da aplicação Auctions.
Organizadas por domínio.
"""

from .auctions import AuctionSerializer, CreateListingSerializer
from .auth import LoginSerializer, RegisterSerializer
from .bids import BidSerializer
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
    
    # Comments
    'AddCommentSerializer',
    'CommentsSerializer',
    
    # Watchlist
    'WatchlistAddAuctionSerializer',
    'WatchlistSerializer',
    
    # Categories
    'CategorySerializer'
]
