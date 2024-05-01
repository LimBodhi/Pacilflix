from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_login(request):
    query_str = "SELECT * FROM DAFTAR_UNDUHAN"
    hasil = query(query_str)
    return render(request, 'index.html', {'akun': hasil})