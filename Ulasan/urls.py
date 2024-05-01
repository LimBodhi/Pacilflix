from django.urls import path
from Ulasan.views import *

apps = 'Ulasan'

urlpatterns = [
    path('', show_ulasan, name='show_ulasan'),
]