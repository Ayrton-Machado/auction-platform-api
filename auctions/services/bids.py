# services/bid_service.py
from django.db import transaction
from django.shortcuts import get_object_or_404
from ..models import AuctionListing, Bids

class BidService:        
    @staticmethod
    @transaction.atomic
    def place_bid(listingData, user, amount):
        if listingData.createdBy == user:
            raise PermissionError("Owner cannot bid on own auction.")
        
        highest_bid = Bids.objects.filter(bidItem=listingData).order_by('-bid').first()
        if highest_bid and highest_bid.bidUser == user:
            raise PermissionError("User cannot increase your own bid, if that is the highest.")

        if amount <= listingData.bidstart:
            raise ValueError(f"Bid must be higher than current bid of R$ {listingData.bidstart}.")

        if listingData.closed:
            raise ValueError("Auction is closed.")
        
        bid_obj, created = Bids.objects.update_or_create(
            bidUser=user,
            bidItem=listingData,
            defaults={'bid': amount}
        )
        
        listingData.bidstart = amount
        listingData.save()
        return bid_obj