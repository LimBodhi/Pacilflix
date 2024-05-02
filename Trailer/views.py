from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_trailer(request):
    query_str = "SELECT * FROM TAYANGAN"
    hasil = query(query_str)
    return render(request, 'index.html', {'trailers': hasil})

def show_search(request):
    query_str = """ SELECT tayangan.judul, tayangan.sinopsis_trailer, tayangan.url_video_trailer, tayangan.release_date_trailer 
                    FROM TAYANGAN
                    WHERE tayangan.judul LIKE '%{query}%'
                    """
    hasil = query(query_str)
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'search.html', {'trailers': hasil})
