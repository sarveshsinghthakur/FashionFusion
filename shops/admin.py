from django.contrib import admin
from .models import products,Contact,checkout,Tracker

admin.site.register(products)
admin.site.register(Contact)
admin.site.register(checkout)
admin.site.register(Tracker)

