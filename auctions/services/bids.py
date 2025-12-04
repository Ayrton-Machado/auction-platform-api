# services/bid_service.py
from django.db import transaction
from ..models import Bids

class BidService:        
    @staticmethod
    @transaction.atomic
    def place_bid(listing, user, amount):
        if listing.created_by == user:
            raise PermissionError("Owner cannot bid on own auction.")
        
        highest_bid = Bids.objects.filter(listing=listing).order_by('-amount').first()
        if highest_bid and highest_bid.user == user:
            raise PermissionError("User cannot increase your own bid, if that is the highest.")

        if listing.winning_bid:
            if amount <= listing.winning_bid:
                raise ValueError(f"Bid must be higher than current bid of R$ {listing.winning_bid}.")

        if amount <= listing.starting_bid:
            raise ValueError(f"Bid must be higher than current bid of R$ {listing.starting_bid}.")

        if listing.closed:
            raise ValueError("Auction is closed.")
        
        bid_obj, created = Bids.objects.update_or_create(
            user=user,
            listing=listing,
            defaults={'amount': amount}
        )
        
        listing.winning_bid = amount
        listing.save()
        return bid_obj