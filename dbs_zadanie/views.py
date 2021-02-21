from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


def index(request):
    return HttpResponse("Hello, world.")
