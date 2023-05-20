from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Biding, Comment, Watchlist

ctgs = ['tech', 'fashion', 'household', 'automobile'] #list of all category 

def index(request):
    listings = Listing.objects.filter(isactive=True)
    return render(request, "auctions/index.html", {
        'listings': listings,
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

@login_required(login_url='login')    
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        img_url = request.POST['img_url'] or 'https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-6.png'
        price = request.POST['price']
        category = request.POST['category'] or None
        user = User.objects.get(pk=request.user.id)
        lisiting = Listing(title=title, description=description, img_url=img_url, price=price, category=category, user=user)
        lisiting.save()
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'auctions/create.html',{'categories':ctgs})

@login_required(login_url='login')
def view(request, id):
    listing = Listing.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        bid = Biding(listing=listing, user=user, bid=request.POST['bid'])
        bid.save()
        return HttpResponseRedirect(reverse('view', args=(id,)))
    try:
        watchlist = Watchlist.objects.get(listing=listing, user=user)
    except :
        watchlist = None
    try:
        bid = Biding.objects.filter(listing=listing).order_by('-bid')
        total_bids = len(bid)
        bid = bid.first()
    except:
        total_bids=0
        bid = None
    try:
        comments = Comment.objects.filter(listing=listing)
    except:
        comments = None
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        'watchlist': watchlist,
        'bid':bid,
        'total':total_bids,
        'comments': comments
        })

@login_required(login_url='login')
def toggle_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    try:
        wl = Watchlist.objects.get(listing=listing, user=user)
        wl.delete()
    except:
        wl = Watchlist(listing=listing, user=user)
        wl.save()
    return HttpResponseRedirect(reverse('view', args=(id,)))

@login_required(login_url='login')
def watchlist(request):
    user=User.objects.get(id=request.user.id)
    wl = Watchlist.objects.filter(user=user)
    return render(request,"auctions/watchlist.html", {"watchlists":wl})

@login_required(login_url="login")
def categories(request):
    return render(request, 'auctions/categories.html', {"categories":ctgs})

@login_required(login_url='login')
def category_listing(request, category):
    listing = Listing.objects.filter(category=category)
    return render(request, 'auctions/categories_listing.html', {"listings":listing, 'category':category})

@login_required(login_url="login")
def comment(request, id):
    comment = request.POST["comment"]
    user = User.objects.get(pk=request.user.id)
    listing = Listing.objects.get(pk=id)
    cmt = Comment(comment=comment, user=user, listing=listing)
    cmt.save()
    return HttpResponseRedirect(reverse('view', args=(id,)))


@login_required(login_url='login')
def close(request, id):
    user = User.objects.get(pk=request.user.id)
    close = Listing.objects.get(user=user, pk=id)
    close.isactive = False
    close.save()
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='login')
def bids(request):
    user = User.objects.get(pk=request.user.id)
    bids = Biding.objects.filter(user=user)
    return render(request, 'auctions/bids.html', {
        'bids':bids
    })

@login_required(login_url='login')
def selling(request):
    user = User.objects.get(pk=request.user.id)
    active_sellings = Listing.objects.filter(user=user, isactive=True)
    close_sellings = Listing.objects.filter(user=user, isactive=False)
    return render(request, 'auctions/selling.html', {
        'actives':active_sellings,
        'closeds' : close_sellings
    })