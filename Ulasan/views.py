import datetime
from django.shortcuts import render
from django.db.backends.utils import CursorWrapper

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

def add_ulasan_film(cursor: CursorWrapper, request):
    current_time = datetime.datetime.now()
    username = request.session['username']
    id_tayangan = request.POST.get('id_film')
    rating = request.POST.get('rating')
    deskripsi = request.POST.get('deskripsi')
    cursor.execute(f"INSERT INTO ulasan (username, id_tayangan, timestamp, rating, deskripsi) VALUES ({username}, {id_tayangan}, {current_time}, {rating}, {deskripsi});")
    return redirect('Tayangan:film.html')

def add_ulasan_series(cursor: CursorWrapper, request):
    current_time = datetime.datetime.now()
    username = request.session['username']
    id_tayangan = request.POST.get('id_series')
    rating = request.POST.get('rating')
    deskripsi = request.POST.get('deskripsi')
    cursor.execute(f"INSERT INTO ulasan (username, id_tayangan, timestamp, rating, deskripsi) VALUES ({username}, {id_tayangan}, {current_time}, {rating}, {deskripsi});")
    return redirect('Tayangan:series.html')
