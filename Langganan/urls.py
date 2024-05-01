from django.urls import path
from Langganan.views import *

apps = 'Langganan'

urlpatterns = [
    path('', langganan_list, name='langganan_list'),
    path('beli/<str:nama_paket>/', beli_paket, name='beli_paket'),
    path('proses_pembayaran/', proses_pembayaran, name='proses_pembayaran')
]