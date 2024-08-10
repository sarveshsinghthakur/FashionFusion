
from django.urls import path
from . import views


urlpatterns = [
    path("shops",views.shops, name = "shops"),
    path("category/<str:cat>",views.categories, name = "Categories"),
    path("about",views.about, name = "about"),
    path("cart",views.cart, name = "cart"),  
    path("product/<int:id>",views.product, name = "product"), 
    path("contact",views.contact, name = "contact"), 
    path("Tracker",views.Tracker_view, name = "Tracker"), 
    path("search",views.search, name ="search"),
  
    
]
