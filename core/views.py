#from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Olá! Esta é minha primeira página em Django.")
