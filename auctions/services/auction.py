from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from ..models import AuctionListing, Bids


class AuctionService:
    @staticmethod
    @transaction.atomic
    def close_auction(auction, lastBid):
        if auction.closed:
            raise ValueError("Auction already closed.")
        
        
        return auction