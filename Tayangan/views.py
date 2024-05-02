from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_tayangan(request):
    query_str = "SELECT * FROM TAYANGAN LIMIT 10;"
    hasil = query(query_str)
    query_str_film = "SELECT * FROM TAYANGAN JOIN FILM ON film.id_tayangan = tayangan.id;"
    hasil_film = query(query_str_film)
    query_str_series = "SELECT * FROM TAYANGAN JOIN SERIES ON series.id_tayangan = tayangan.id;"
    hasil_series = query(query_str_series)
    # for data in hasil:
    #     data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'tayangan.html', {'tayangans': hasil, 'tayangan_film': hasil_film, 'tayangan_series': hasil_series})

def show_search_tayangan(request):
    query_str = """ SELECT tayangan.judul, tayangan.sinopsis_trailer, tayangan.url_video_trailer, tayangan.release_date_trailer 
                    FROM TAYANGAN
                    WHERE tayangan.judul LIKE '%{query}%';
                    """
    hasil = query(query_str)
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'search_tayangan.html', {'tayangans': hasil})

def show_film(request):
    id_film = request.POST.get('id_film')
    query_str = f"SELECT * FROM TAYANGAN JOIN FILM ON film.id_tayangan = tayangan.id WHERE id_tayangan = '{id_film}';"
    hasil = query(query_str)
    # for data in hasil:
    #     data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'film.html', {'films': hasil})

def show_series(request):
    id_series = request.POST.get('id_series')
    query_str = f"SELECT * FROM TAYANGAN JOIN SERIES ON series.id_tayangan = tayangan.id WHERE id_tayangan = '{id_series}';"
    hasil = query(query_str)
    # for data in hasil:
    #     data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'series.html', {'series': hasil})

def show_episode(request):
    query_str = "SELECT * FROM TAYANGAN JOIN SERIES ON series.id_tayangan = tayangan.id JOIN EPISODE ON episode.id_series = series.id_tayangan;"
    hasil = query(query_str)
    # for data in hasil:
    #     data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'episode.html', {'episode': hasil})