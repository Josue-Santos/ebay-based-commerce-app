from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import User,Listing,WatchList,Bid,Comment



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

def index(request):
    count = 0
    user = request.user
    watchlist= WatchList.objects.all()
    for x in watchlist:
        if x.user.username == user.username:
            count +=1
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listings": listings,
        "count":count
    })



def categories(request):
    count = 0
    user = request.user
    watchlist= WatchList.objects.all()
    for x in watchlist:
        if x.user.username == user.username:
            count +=1

   
    return render(request, "auctions/categories.html", {
        "user": user,
        "count":count,
        
    })

def category(request, category):
    ##Watchlist Info
    count = 0
    user = request.user
    watchlist= WatchList.objects.all()
    for x in watchlist:
        if x.user.username == user.username:
            count +=1

    listings = Listing.objects.all()       
    return render(request, "auctions/category.html",{
        "user": user,
        "watchlist":watchlist,
        "count":count,
        "listings":listings,
        "category":category
    })
def user(request,listed_by):
     ##Watchlist Info
    count = 0
    user = request.user
    watchlist= WatchList.objects.all()
    for x in watchlist:
        if x.user.username == user.username:
            count +=1
    
    listings = Listing.objects.all() 
    
    return render(request, "auctions/user.html",{
        "user":user,
        "watchlist":watchlist,
        "count":count,
        "listings":listings,
        "listed_by":listed_by
    })
        

def watchlist(request,user):
    count = 0
    user = request.user
    watchlist= WatchList.objects.all()
    for x in watchlist:
        if x.user.username == user.username:
            count +=1
    return render(request, "auctions/watchlist.html",{
         "user": user,
         "watchlist":watchlist,
         "count":count
    })

def addtowatchlist(request,listing_id):
    count = 0
    found = False
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    w = WatchList(user = user, listing =listing)
    watchlist = WatchList.objects.all()
    if len(watchlist) == 0:
        w.save()

    if len(watchlist) >0:
        for x in watchlist:
            if x.user.username == user.username and x.listing.id == listing_id:
                found = True
        for x in watchlist:
            if x.user.username == user.username:
                count +=1
        if  found == False:
            w.save()   
    
    watchlist= WatchList.objects.all()
    #Redirect User to watchlist
    return render(request,"auctions/watchlist.html",{
            "user": user,
            "watchlist":watchlist,
            "count":count
    })

def removefromwatchlist(request,user,listing_id):
    count = 0
    user = request.user
    watchlist= WatchList.objects.all()
    for x in watchlist:
        if x.user.username == user.username:
            count +=1

    listings = Listing.objects.all()

    ##removing item from watchlist
    for x in watchlist:
        if x.user.username == user.username and x.listing.id == listing_id:
            x.delete()
            count -=1
    watchlist= WatchList.objects.all()
    return render(request, "auctions/watchlist.html",{
        "user": user,
        "watchlist":watchlist,
        "count":count,
    })

def create(request):
    count = 0
    user = request.user
    watchlist= WatchList.objects.all()
    for x in watchlist:
        if x.user.username == user.username:
            count +=1

    if request.method =="POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image"]
        category = request.POST["category"]
        listed_by = request.user.username
        sold = "False"
        listing = Listing(user = user,title =title,description=description,
                          starting_bid=starting_bid,image=image,
                          category=category, listed_by=listed_by, sold=sold)
        
        listing.save()
        #Redirect User to Index
        return HttpResponseRedirect(reverse("index"))

    return render(request,"auctions/create.html",{
        "count":count,
    })

def comment(request,listing_id):
    #counting items on Watchlist
    count = 0
    user = request.user
    watchlist= WatchList.objects.all()
    for x in watchlist:
        if x.user.username == user.username:
            count +=1
    ##Getting listing
    listing = Listing.objects.get(id=listing_id)

    #creating found variable
    found = False
    #variable to check if item is sold or not
    sold = listing.sold
    for x in watchlist:
        if x.user.username == user.username:
            count +=1
        if x.listing.id == listing.id and x.user.username == user.username:
            found = True
    #message
    message=""

    ##checking if current user was the one who created the list
    ## so that we can easily add a close listing option once user wants to sell
    current_user_listing = False
    if user.username == listing.user.username:
        current_user_listing = True
    ##counting bids
    bids= Bid.objects.all()
    bid_counter = 0
    
    for x in bids:
        if listing_id == x.listing.id:
            bid_counter+=1

    ##getting max_bid
    max_bid = 0
    for x in bids:
        if x.listing.id == listing_id:
            if x.new_bid > max_bid:
                max_bid = x.new_bid
            
     ##checking if user has current max_bid
    current_max_bid_user =""
    current_max_bid = False
    for x in bids:
        if user.username == x.user.username and max_bid == x.new_bid:
            current_max_bid = True
            current_max_bid_user = user.username

    if request.method == "POST":
        #getting information from form
        listing = Listing.objects.get(id=listing_id)
        comment = request.POST["comment"]
        #Saving comment
        new = Comment(listing=listing, user=user, comment =comment)
        new.save()
        ##Getting comments 
        comments = Comment.objects.all()
        ##Redirecting to Listing
   
        return render(request, "auctions/listing.html", {
            "user": user,
            "listing": listing,
            "count":count,
            "watchlist":watchlist,
            "found":found,
            "message":message,
            "bids": bids,
            "bid_counter":bid_counter,
            "max_bid":max_bid,
            "current_max_bid":current_max_bid,
            "current_user_listing":current_user_listing,
            "sold":sold,
            "current_max_bid_user":current_max_bid_user,
            "comments":comments
        })


def listing(request, listing_id):
 
    #counting items on Watchlist
    count = 0
    user = request.user
    watchlist= WatchList.objects.all()
    for x in watchlist:
        if x.user.username == user.username:
            count +=1
  
    listing = Listing.objects.get(id=listing_id)

    ##Getting comments 
    comments = Comment.objects.all()

    ##creating found variable
    found = False
    #variable to check if item is sold or not
    sold = listing.sold
    for x in watchlist:
        if x.listing.id == listing.id and x.user.username == user.username:
            found = True

    ##checking if current user was the one who created the list
    ## so that we can easily add a close listing option once user wants to sell
    current_user_listing = False
    if user.username == listing.user.username:
        current_user_listing = True
    ##counting bids
    bids= Bid.objects.all()
    bid_counter = 0
    
    for x in bids:
        if listing_id == x.listing.id:
            bid_counter+=1

    ##getting max_bid
    max_bid = 0
    for x in bids:
        if x.listing.id == listing_id:
            if x.new_bid > max_bid:
                max_bid = x.new_bid
            
     ##checking if user has current max_bid
    current_max_bid_user =""
    current_max_bid = False
    for x in bids:
        if user.username == x.user.username and max_bid == x.new_bid:
            current_max_bid = True
            current_max_bid_user = user.username
    ##Placing a bid
    if request.method =="POST":
        user = request.user
        listing = Listing.objects.get(id=listing_id)
        starting_bid = listing.starting_bid
        new_bid = float(request.POST["new_bid"])
        message = "New bid has to be greater than current bid and starting price."

    

        ##To check if new bid is valid
        if new_bid <= starting_bid or new_bid <= max_bid:
            return render(request, "auctions/listing.html", {
            "user": user,
            "listing": listing,
            "count":count,
            "watchlist":watchlist,
            "found":found,
            "message":message,
            "bids": bids,
            "bid_counter":bid_counter,
            "max_bid":max_bid,
            "current_max_bid":current_max_bid,
            "current_user_listing":current_user_listing,
            "sold":sold,
            "current_max_bid_user":current_max_bid_user,
            "comments":comments

        })
        ##When new bid is valid
        if new_bid > max_bid:
            max_bid =new_bid
            bid_counter +=1
            message=""
            current_max_bid = True
            bid = Bid(user=user,listing=listing,new_bid=new_bid)
            bid.save()
            #Redirect User to Listing.html
            return render(request, "auctions/listing.html", {
                "user": user,
                "listing": listing,
                "count":count,
                "watchlist":watchlist,
                "found":found,
                "message":message,
                "bids": bids,
                "bid_counter":bid_counter,
                "max_bid":max_bid,
                "current_max_bid":current_max_bid,
                "current_user_listing":current_user_listing,
                "sold":sold,
                "current_max_bid_user":current_max_bid_user,
                "comments":comments

        })
            
    ##request method == GET 
    return render(request, "auctions/listing.html", {
        "user": user,
        "listing": listing,
        "count":count,
        "watchlist":watchlist,
        "found":found,
        "bid_counter":bid_counter,
        "max_bid":max_bid,
        "current_max_bid":current_max_bid,
        "current_user_listing":current_user_listing,
        "sold":sold,
        "current_max_bid_user":current_max_bid_user,
        "comments":comments

    })
    
def sell(request,listing_id):
    #counting items on Watchlist
    count = 0
    found = False
    user = request.user
    watchlist= WatchList.objects.all()
    listing = Listing.objects.get(id=listing_id)
    for x in watchlist:
        if x.user.username == user.username:
            count +=1
        if x.listing.id == listing.id and x.user.username == user.username:
            found = True

    ##Getting comments 
    comments = Comment.objects.all()

    #We need to change te listing so that our column sold is true instead of false!
    sold = "True"
    message = ""
    Listing.objects.filter(pk=listing_id).update(sold='True')

     ##counting bids
    bids = Bid.objects.all()
    bid_counter = 0
    
    for x in bids:
        if listing_id == x.listing.id:
            bid_counter+=1

    ##getting max_bid
    max_bid = 0
    for x in bids:
        if x.listing.id == listing_id:
            if x.new_bid > max_bid:
                max_bid = x.new_bid

    ##checking if user has current max_bid
    current_max_bid_user =""
    current_max_bid = False
    for x in bids:
        if user.username == x.user.username and max_bid == x.new_bid:
            current_max_bid = True
            current_max_bid_user = user.username

    ##checking if current user was the one who created the list
    ## so that we can easily add a close listing option once user wants to sell
    current_user_listing = False
    if user.username == listing.user.username:
        current_user_listing = True

    return render(request, "auctions/listing.html", {
        "user": user,
        "listing": listing,
        "count":count,
        "watchlist":watchlist,
        "found":found,
        "bid_counter":bid_counter,
        "max_bid":max_bid,
        "current_max_bid":current_max_bid,
        "current_user_listing":current_user_listing,
        "sold":sold,
        "current_max_bid_user":current_max_bid_user,
        "comments":comments

    })
