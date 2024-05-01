from django.urls import path
from LoginDanLogout.views import *

app_name = 'LoginDanLogout'

urlpatterns = [
    path('', show_main, name="show_main"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]