from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_trailer(request):
    query_str = """ WITH ValidViews AS (
                        SELECT 
                            rn.id_tayangan,
                            COUNT(*) AS total_view
                        FROM 
                            RIWAYAT_NONTON rn
                        JOIN 
                            TAYANGAN t ON rn.id_tayangan = t.id
                        WHERE 
                            rn.end_date_time > rn.start_date_time
                            AND rn.end_date_time >= NOW() - INTERVAL '7 days'
                            AND EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) >= 0.7 * (EXTRACT(EPOCH FROM (t.durasi * INTERVAL '1 minute')))
                        GROUP BY 
                            rn.id_tayangan
                    )
                    SELECT generate_series(1, 10) AS peringkat, 
                    tayangan.judul, 
                    tayangan.sinopsis_trailer, 
                    tayangan.url_video_trailer, 
                    tayangan.release_date_trailer,
                    vv.total_view as total_view
                    FROM ValidViews vv
                    JOIN TAYANGAN t on vv.id_tayangan = t.id
                    ORDER BY vv.total_view DESC
                    LIMIT 10;"""
    hasil = query(query_str)
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    query_str_film = "SELECT * FROM TAYANGAN JOIN FILM ON film.id_tayangan = tayangan.id;"
    hasil_film = query(query_str_film)
    query_str_series = "SELECT * FROM TAYANGAN JOIN SERIES ON series.id_tayangan = tayangan.id;"
    hasil_series = query(query_str_series)
    return render(request, 'trailer.html', {'trailers': hasil, 'films': hasil_film, 'series':hasil_series})

def show_search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search')
    query_str = f" SELECT tayangan.judul, tayangan.sinopsis_trailer, tayangan.url_video_trailer, tayangan.release_date_trailer FROM TAYANGAN WHERE tayangan.judul LIKE '%{search_query}%';"
    hasil = query(query_str)
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'search.html', {'trailers': hasil})
