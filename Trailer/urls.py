from django.urls import path
from Trailer.views import *

apps = 'Trailer'

urlpatterns = [
    path('', show_trailer, name='show_trailer'),
    path('search/', show_search, name='show_search'),
]