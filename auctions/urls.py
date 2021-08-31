from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories" ,views.categories, name ="categories"),
    path("<str:user>/watchlist" ,views.watchlist, name ="watchlist"),
    path("<int:listing_id>/watchlist/",views.addtowatchlist, name="addtowatchlist"),
    path("<str:user>/<int:listing_id>/watchlist/",views.removefromwatchlist,name="removefromwatchlist"),
    path("create" ,views.create, name ="create"),
    path("<int:listing_id>",views.listing, name ="listing"),
    path("listings/<str:category>",views.category,name="category"),
    path("user/<str:listed_by>",views.user,name="user"),
    path("sell/<int:listing_id>",views.sell,name="sell"),
    path("comment/<int:listing_id>",views.comment,name="comment")
    
]

