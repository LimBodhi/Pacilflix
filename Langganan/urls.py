from django.urls import path
from Langganan.views import *

apps = 'Langganan'

urlpatterns = [
    path('', show_akun, name='show_akun'),
]