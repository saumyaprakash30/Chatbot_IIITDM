from django.http.response import HttpResponse
from django.shortcuts import render
from .ml import predict

# Create your views here.

def chat(request):
    message = request.GET['message']
    print(message)
    tag = predict(message)

    return HttpResponse(tag)