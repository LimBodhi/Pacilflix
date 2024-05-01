from django.urls import path
from DaftarUnduhan.views import *

apps = 'DaftarUnduhan'

urlpatterns = [
    path('', show_unduhan, name='show_unduhan'),
    path('remove/', remove_unduhan, name='remove_unduhan'),
]