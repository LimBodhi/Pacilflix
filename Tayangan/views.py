from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_tayangan(request):
    query_str = "SELECT * FROM TAYANGAN"
    hasil = query(query_str)
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'tayangan.html', {'tayangans': hasil})

def show_search(request):
    query_str = """ SELECT tayangan.judul, tayangan.sinopsis_trailer, tayangan.url_video_trailer, tayangan.release_date_trailer 
                    FROM TAYANGAN
                    WHERE tayangan.judul LIKE '%{query}%'
                    """
    hasil = query(query_str)
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'search.html', {'tayangans': hasil})

def show_film(request):
    query_str = "SELECT * FROM TAYANGAN JOIN FILM ON film.id_tayangan = tayangan.id"
    hasil = query(query_str)
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'film.html', {'films': hasil})

def show_series(request):
    query_str = "SELECT * FROM TAYANGAN JOIN SERIES ON series.id_tayangan = tayangan.id"
    hasil = query(query_str)
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'series.html', {'series': hasil})

def show_episode(request):
    query_str = "SELECT * FROM TAYANGAN JOIN EPISODE ON episode.id_series = tayangan.id"
    hasil = query(query_str)
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'episode.html', {'episodes': hasil})