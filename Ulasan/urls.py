from django.urls import path
from Ulasan.views import *

apps = 'Ulasan'

urlpatterns = [
    path('', show_ulasan, name='show_ulasan'),
    path('add_ulasan_film/', add_ulasan_film, name='add_ulasan_film'),
    path('add_ulasan_series/', add_ulasan_series, name='add_ulasan_series'),
]