from django.urls import path
from LoginDanLogout.views import *

apps = 'LoginDanLogout'

urlpatterns = [
    path('', show_login, name='show_login'),
]