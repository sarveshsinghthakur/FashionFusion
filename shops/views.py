from django.shortcuts import render
from django.http import JsonResponse
from .models import products, Contact, checkout, Tracker 
from math import ceil
import logging
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)

def shops(request):
    allprods = []
    cate = products.objects.values('category', 'product_id')
    cats = {items['category'] for items in cate}
    for cat in cats:
        prods = products.objects.filter(category=cat)
        n = len(prods)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prods, range(1, nslides), nslides])
    unique_categories = {products[0].category for products, range, nslides in allprods}
    params = {'allprods': allprods, 'unique': unique_categories}
    return render(request, 'shops/shop.html', params)

def searchmatch(query, item):
    query = query.lower()
    return query in item.product_name.lower() or query in item.desc.lower() or query in item.category.lower()

def search(request):
    query = request.GET.get('search', '')
    allprods = []
    unique_categories = set()

    if query and len(query) >= 3:
        cate = products.objects.values('category', 'product_id')
        cats = {item['category'] for item in cate}

        for cat in cats:
            prods = products.objects.filter(category=cat)
            prodres = [item for item in prods if searchmatch(query, item)]
            n = len(prodres)
            if n > 0:
                nslides = n // 4 + ceil((n / 4) - (n // 4))
                allprods.append([prodres, range(1, nslides + 1), nslides])
                unique_categories.add(cat)
    else:
        params = {'msg': "Enter a relevant query to search"}
        return render(request, 'shops/search.html', params)
                
    params = {'allprods': allprods, 'unique': unique_categories}
    if not allprods:
        params = {'msg': "No results found for your query"}
        
    return render(request, 'shops/search.html', params)

def categories(request, cat):
    allprods = []
    prods = products.objects.filter(category=cat)
    n = len(prods)
    nslides = n // 4 + ceil((n / 4) - (n // 4))
    allprods.append([prods, range(1, nslides), nslides])
    unique_categories = {products[0].category for products, range, nslides in allprods}
    params = {'allprods': allprods, 'unique': unique_categories}
    return render(request, 'shops/categories.html', params)

def about(request):
    return render(request, 'shops/about.html')

def cart(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        try:
            amount = float(amount)
        except ValueError:
            amount = 0
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zipcode', '')
        Checkout = checkout(items_json=items_json, name=name, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code , amount=amount)
        print(amount)
        Checkout.save()
        Track = Tracker(order=Checkout, update_desc="The order has been placed") 
        Track.save()
        thank = True
        id = Checkout.order_number
        return render(request, 'shops/cart.html', {'thank': thank, 'id': id})
    return render(request, 'shops/cart.html')

def product(request, id):
    product = products.objects.filter(product_id=id)
    return render(request, 'shops/product.html', {'product': product})

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        number = request.POST.get('number', '')
        query = request.POST.get('query', '')
        contacts = Contact(name=name, email=email, number=number, query=query)
        contacts.save()
    return render(request, 'shops/contact.html')

def Tracker_view(request):
    if request.method == 'POST':
        logger.info("Received POST request: %s", request.POST)
        order_number = request.POST.get('order_number')
        email = request.POST.get('email')
        logger.info("Order number: %s, Email: %s", order_number, email)

        try:
            order = checkout.objects.get(order_number=order_number, email=email)
            updates = Tracker.objects.filter(order=order)
            response_data = [
                {'text': update.update_desc, 'time': update.timestamp.strftime('%d-%m-%Y')}
                for update in updates
            ]
            return JsonResponse(response_data, safe=False)
        except checkout.DoesNotExist:
            logger.error("Order does not exist")
            return JsonResponse([], safe=False)
    logger.error("Invalid request method")
    return render(request, 'shops/Tracker.html')
