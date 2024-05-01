from django.urls import path
from Pengguna.views import *

apps = 'Pengguna'

urlpatterns = [
    path('', show_pengguna, name='show_pengguna'),
]