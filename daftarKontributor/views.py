from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_kontributor(request):
    query_str = "SELECT * FROM DAFTAR_UNDUHAN"
    hasil = query(query_str)
    return render(request, 'index.html', {'akun': hasil})