from django.urls import path
from .views import nerest_gym

urlpatterns = [
    path('nerestGym/',nerest_gym,name="nearby_gym")
]
