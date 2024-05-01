from django.urls import path
from Pengguna.views import *

app_name = 'Pengguna'

urlpatterns = [
    path("", register, name="register"),
]