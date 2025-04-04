#from django.shortcuts import render
from .models import Gym
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests 
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # Radius of Earth in kilometers 
    r = 6371  
    return c * r


@api_view(['GET'])

def nerest_gym(request):
    try:
        user_latitude = float(request.GET.get('latitude'))
        user_longitude = float(request.GET.get('longitude'))
    except (TypeError , ValueError):
        return Response ({'error': 'Invalid entry(check latitude and longitude)'},status=400)
    
    SerpApiKey = "" #we need to serp Api Key
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_maps",
        "q": "gyms",
        "ll": f"@{user_latitude},{user_longitude},15z",  
        #"location": "Chennai, India",  
        "google_domain": "google.co.in",  
        "radius": 4000,  
        "api_key": SerpApiKey
    }
    response = requests.get(url,params=params)
    data = response.json()

    if "local_results" not in data or not data["local_results"]:
        return Response({"Error_message": "No gyms found near the provided location"}, status=404)
    
    
    gyms = [
        {
            "name": gym["title"],
            "address": gym.get("address", "Address not available"),
            "rating": gym.get("rating", "N/A"),
            "distance_km": round(haversine(
            user_latitude, user_longitude,
            gym["gps_coordinates"]["latitude"], gym["gps_coordinates"]["longitude"]
        ), 2)
        }
        for gym in data["local_results"]
    ]
    gyms.sort(key=lambda x: x['distance_km'])

    return Response({"gyms": gyms})