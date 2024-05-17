from django.urls import path
from .views import show_favorit, remove_favorit, show_favorit_detail

urlpatterns = [
    path('', show_favorit, name='show_favorit'),
    path('remove/', remove_favorit, name='remove_favorit'),
    path('<str:judul>/', show_favorit_detail, name='show_favorit_detail'),
]