from django.urls import path
from daftarKontributor.views import *

apps = 'DaftarKontributor'

urlpatterns = [
    path('', show_kontributor, name='show_kontributor'),
]