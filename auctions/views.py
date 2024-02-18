from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, AuctionListing

class Auction_Listing(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'bidstart', 'urlImage', 'category']
        
    def __init__(self, *args, **kwargs):
        super(Auction_Listing, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

def index(request):
    auctions = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        'auctions': auctions
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    auction = Auction_Listing(request.POST)
    if request.method == 'POST':
        auction = Auction_Listing(request.POST)
        if auction.is_valid():
            auction.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'auctions/createlisting.html', {
        'auction': auction
    })