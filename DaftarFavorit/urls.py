from django.urls import path
from DaftarFavorit.views import *

apps = 'DaftarFavorit'

urlpatterns = [
    path('', show_favorit, name='show_favorit'),
    path('remove/', remove_favorit, name='remove_favorit'),
]