from django.urls import path
from Trailer.views import *

apps = 'Trailer'

urlpatterns = [
    path('', show_trailer, name='show_trailer'),
]