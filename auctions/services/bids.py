# services/bid_service.py
from django.db import transaction
from ..models import Bids

class BidService:        
    @staticmethod
    @transaction.atomic
    def place_bid(listingData, user, amount):
        if listingData.created_by == user:
            raise PermissionError("Owner cannot bid on own auction.")
        
        highest_bid = Bids.objects.filter(listing=listingData).order_by('-amount').first()
        if highest_bid and highest_bid.user == user:
            raise PermissionError("User cannot increase your own bid, if that is the highest.")

        if amount <= listingData.starting_bid:
            raise ValueError(f"Bid must be higher than current bid of R$ {listingData.starting_bid}.")

        if listingData.closed:
            raise ValueError("Auction is closed.")
        
        bid_obj, created = Bids.objects.update_or_create(
            user=user,
            listing=listingData,
            defaults={'amount': amount}
        )
        
        listingData.starting_bid = amount
        listingData.save()
        return bid_obj