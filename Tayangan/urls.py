from django.urls import path
from Tayangan.views import *

apps = 'Tayangan'

urlpatterns = [
    path('', show_tayangan, name='show_tayangan'),
    path('search/', show_search, name='show_search'),
    path('film/', show_film, name='show_film'),
    path('series/', show_series, name='show_series'),
    path('episode/', show_episode, name='show_episode'),
]