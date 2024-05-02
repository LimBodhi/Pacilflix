from django.urls import path
from Tayangan.views import *

apps = 'Tayangan'

urlpatterns = [
    path('', show_tayangan, name='show_tayangan'),
    path('search/', show_search, name='show_search'),
]