from django.urls import path
from Tayangan.views import *

app_name = 'Tayangan'

urlpatterns = [
    path('', show_tayangan, name='show_tayangan'),
    path('search_tayangan/', show_search_tayangan, name='show_search_tayangan'),
    path('halaman_tayangan/', show_halaman_tayangan, name='show_halaman_tayangan'),
    path('film/', show_film, name='show_film'),
    path('series/', show_series, name='show_series'),
    path('episode/', show_episode, name='show_episode'),
]