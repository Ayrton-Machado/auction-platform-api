from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from ..models import AuctionListing, Category, Bids
from django.core.exceptions import ValidationError, PermissionDenied


class AuctionService:
    @staticmethod
    @transaction.atomic
    def close_auction(listing, last_bid_user, last_bid_amount, requesting_user):
        if listing.closed:
            raise ValidationError("Auction already closed.")

        if requesting_user != listing.created_by:
            raise PermissionDenied("Only the auction owner can close it.")
            
        listing.closed = True
        listing.winner = last_bid_user
        listing.winning_bid = last_bid_amount
        listing.save()

        return listing

    @staticmethod
    @transaction.atomic
    def create_listing(listing_data, user):
        print(listing_data)
        if 'category' not in listing_data or listing_data['category'] is None:
            listing_data['category'] = Category.objects.get(name="Outro")

        listing_data['created_by'] = user
        auction_obj = AuctionListing.objects.create(**listing_data)

        return auction_obj