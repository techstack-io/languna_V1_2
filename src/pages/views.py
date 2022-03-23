from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'pages/index.html')

def models(request):
    return render(request, 'pages/models.html')

def count(request):
    return render(request, 'pages/count.html')
    fulltext = request.GET['fulltext', {'fulltext': fulltext}]
