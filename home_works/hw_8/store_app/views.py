from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello from main store page")

def about(request):
    return HttpResponse("About the store")