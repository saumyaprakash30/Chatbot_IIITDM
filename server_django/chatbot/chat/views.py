from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
from .ml import predict
import json
# Create your views here.

# class ChatBotResponse:
    



def chat(request):
    message = request.GET['message']
    response = predict(message)   
    return JsonResponse(response,safe=False)


def rule(request):

    return "hi this is rule"