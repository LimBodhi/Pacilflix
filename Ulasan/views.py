from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_ulasan(request):
    query_str = ''' SELECT ulasan.username, ulasan.deskripsi, ulasan.rating, ulasan.timestamp 
                    FROM ULASAN 
                    JOIN TAYANGAN ON tayangan.id = ulasan.id_tayangan
                    ORDER BY ulasan.timestamp DESC;
                '''
    hasil = query(query_str)
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'ulasan.html', {'ulasans': hasil})

