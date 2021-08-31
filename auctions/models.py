from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    pass

class Listing(models.Model):

    FASHION = 'F'
    TOYS  = 'T'
    ELECTRONICS = 'E'
    HOME = 'H'
    SPORTS = 'S'
    PETS = 'P'

    CATEGORY_CHOICES = [
      (FASHION,'Fashion'),
      (TOYS,'Toys'),
      (ELECTRONICS,'Electronics'),
      (HOME,'Home'),
      (SPORTS,'Sports'),
      (PETS,'Pets'),
      
    ]
    title = models.CharField(max_length=64,blank=False)
    description = models.TextField(max_length=1000,blank=False)
    starting_bid = models.FloatField(blank=False)
    image = models.CharField(max_length =1000, blank=True)
    category = models.CharField(max_length=13,choices = CATEGORY_CHOICES,blank=True)
    listed_by = models.CharField(max_length=64,blank=True)
    date = models.DateTimeField(auto_now =True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sold = models.CharField(max_length=64,blank=False)
    
    def __str__ (self):
        return f" User: {self.user} {self.title}: {self.description} bid: {self.starting_bid} {self.image} category: {self.category} listed_by: {self.listed_by} date: {self.date} sold:{self.sold}"

class WatchList(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name ="users")
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="listings")

  def __str__(self):
    return f"User: {self.user} Title: {self.listing.title}  Description: {self.listing.description} bid: {self.listing.starting_bid} {self.listing.image}category: {self.listing.category} listed_by: {self.listing.listed_by}  date: {self.listing.date} "

class Bid(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  listing = models.ForeignKey(Listing, on_delete = models.CASCADE)
  new_bid = models.FloatField(blank=False)

  def __str__(self):
    return f"User: {self.user} Listing: {self.listing.title} new_bid = {self.new_bid}"

class Comment(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
  comment = models.TextField(max_length=1500,blank=False)

  def __str__(self):
    return f"User: {self.user} Listing: {self.listing} Comment: {self.comment}"


 