from django.urls import path
from daftarKontributor.views import *

apps = 'daftarKontributor'

urlpatterns = [
    path('', show_kontributor, name='show_kontributor'),
]