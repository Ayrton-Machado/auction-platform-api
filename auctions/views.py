# Autenticação
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # Substitui IsAuthenticated

# Banco de dados
from django.db import IntegrityError
from .models import *
from .serializers import *  # Novo: substitui forms

class indexAPI(APIView):
    def get(self, request):
        auctions = AuctionListing.objects.all()
        return Response({'auctions': list(auctions.values())})

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Attempt to sign user in
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return Response({
                    "message": "Login Successful.",
                    "user": {
                        "username": user.username
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Invalid username and/or password."
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    categories = Category.objects.all()
    if request.method == 'POST':
        # create listing form 
        title = request.POST.get('title')
        description = request.POST.get('description')
        bidstart = request.POST.get('bidstart')
        urlImage = request.POST.get('urlImage')
        createdBy = request.user
        category_item = request.POST.get('category')
        #adicionar categoria ao listamento
        category = Category.objects.get(categories=category_item)
        AuctionListing(title=title, description=description, bidstart=bidstart, urlImage=urlImage, createdBy=createdBy, category=category).save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'auctions/createlisting.html', {
        'categories': categories
    })

def listing(request, listing_id):
    listingItem = AuctionListing.objects.get(id=listing_id)
    allComments = Comments.objects.filter(item=listingItem)
    biditem = Bids.objects.filter(bidItem=listingItem)
    lastBid = Bids.objects.filter(bidItem=listingItem).last()
    if request.user == listingItem.createdBy:
        canClose = True
    else:
        canClose = False
    if lastBid is None:
        return render(request, 'auctions/listing.html', {
            'listing_id': listing_id,
            'listing': listingItem,
            'canClose': canClose,
            'comments': allComments
        })
    user = lastBid.bidUser
    bidAmount = len(biditem)
    if request.user == user:
        win = True
    else:
        win = False
    return render(request, 'auctions/listing.html', {
        'listing_id': listing_id,
        'listing': listingItem,
        'bidlist': biditem,
        'bidAmount': bidAmount,
        'win': win,
        'canClose': canClose,
        'comments': allComments
    })


def watchlist(request):
    user = request.user
    userwatchlist = Watchlist.objects.filter(user=user)
    if request.method == 'POST':
        listing_id = request.POST.get('addWatchlist')
        item = AuctionListing.objects.get(id=listing_id)
        watchlist = Watchlist(user=user, item=item)
        watchlist.save()
        return render(request, 'auctions/watchlist.html', {
            'watchlist': userwatchlist
        })
    return render(request, 'auctions/watchlist.html', {
        'watchlist': userwatchlist
    })

def watchlistRemove(request):
    if request.method == 'POST':
        listing_id = request.POST.get('removeWatchlist')
        item = Watchlist.objects.get(id=listing_id)
        item.delete()
    return HttpResponseRedirect(reverse('watchlist'))

def placeBid(request, listing_id):
    listingItem = AuctionListing.objects.get(id=listing_id)
    bidstart = listingItem.bidstart
    bid = int(request.POST.get('placebid'))
    bidUser = request.user
    if bid > bidstart:
        listingItem.bidstart = bid
        Bids(bidUser=bidUser, bid=bid, bidItem=listingItem).save()
        listingItem.save()
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    else:
        return render(request, 'auctions/error.html')
    
def error(request):
    return render(request, 'auctions/error.html')
    

def closeAuction(request, listing_id):
    listingItem = AuctionListing.objects.get(id=listing_id)
    lastBid = Bids.objects.filter(bidItem=listingItem).last()
    listingItem.closed = True
    listingItem.save()
    close = listingItem.closed
    if close == True:
        if close == True and request.user == lastBid.bidUser:
            winner = True
        elif close == True and request.user != lastBid.bidUser:
            winner = False
        return render(request, 'auctions/auctionclosed.html', {
            'winner': winner
        })
    else:
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    

def addComment(request, listing_id):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        item = AuctionListing.objects.get(id=listing_id)
        user = request.user
        Comments(user=user, item=item, comment=comment).save()
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    
def Categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': categories
    })

def whichCategory(request, which_category):
    user = request.user
    category = Category.objects.get(categories = which_category)
    catAuctions = AuctionListing.objects.filter(category=category)
    allAuctions = AuctionListing.objects.all()
    return render(request, 'auctions/category.html', {
        'catAuctions': catAuctions,
        'auctions': allAuctions,
        'which_category': which_category
    })
