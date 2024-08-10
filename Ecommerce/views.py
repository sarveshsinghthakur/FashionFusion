from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request,"mac.html")
# def index(request):
#     return HttpResponse("request")