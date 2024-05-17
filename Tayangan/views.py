from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_tayangan(request):
    # query_str = """ WITH TotalDurationEpisode AS (
    #                     SELECT
    #                         e.id_series,
    #                         SUM(e.durasi * 60) AS total_duration
    #                     FROM
    #                         EPISODE e
    #                     GROUP BY
    #                         e.id_series
    #                 ), ValidViews AS (
    #                     SELECT 
    #                         rn.id_tayangan,
    #                         COUNT(*) AS total_view
    #                     FROM 
    #                         RIWAYAT_NONTON rn
    #                     JOIN 
    #                         TAYANGAN t ON rn.id_tayangan = t.id
    #                     JOIN
    #                         FILM s ON rn.id_tayangan = s.id_tayangan
    #                     JOIN
    #                         TotalDurationEpisode e ON rn.id_tayangan = e.id_series
    #                     WHERE 
    #                         rn.end_date_time > rn.start_date_time
    #                         AND rn.end_date_time >= NOW() - INTERVAL '7 days'
    #                         AND EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) >= 0.7 * (
    #                             CASE
    #                                 WHEN s.id_tayangan IS NOT NULL THEN s.durasi_film * 60 
    #                                 ELSE e.total_duration
    #                             END
    #                         )
    #                     GROUP BY 
    #                         rn.id_tayangan
    #                 )
    #                 SELECT ROW_NUMBER() OVER (ORDER BY vv.total_view DESC) AS peringkat, 
    #                     t.judul, 
    #                     t.sinopsis_trailer, 
    #                     t.url_video_trailer, 
    #                     t.release_date_trailer,
    #                     vv.total_view as total_view,
    #                     t.id as id_tayangan
    #                 FROM ValidViews vv
    #                 JOIN TAYANGAN t on vv.id_tayangan = t.id
    #                 ORDER BY vv.total_view DESC
    #                 LIMIT 10;
    #                 """
    query_str = """SELECT generate_series(1, 10) AS peringkat, 
                        t.judul, 
                        t.sinopsis_trailer, 
                        t.url_video_trailer, 
                        t.release_date_trailer, 
                        generate_series(1, 10) AS total_view FROM TAYANGAN t LIMIT 10;"""
    hasil = query(query_str)
    # for data in hasil:
    #     data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    query_str_film = "SELECT * FROM TAYANGAN JOIN FILM ON film.id_tayangan = tayangan.id;"
    hasil_film = query(query_str_film)
    query_str_series = "SELECT * FROM TAYANGAN JOIN SERIES ON series.id_tayangan = tayangan.id;"
    hasil_series = query(query_str_series)
    return render(request, 'tayangan.html', {'tayangans': hasil, 'films': hasil_film, 'series':hasil_series})

def show_search_tayangan(request):
    if request.method == 'GET':
        search_query = request.GET.get('search')
    query_str = f" SELECT tayangan.judul, tayangan.sinopsis_trailer, tayangan.url_video_trailer, tayangan.release_date_trailer FROM TAYANGAN WHERE tayangan.judul LIKE '%{search_query}%';"
    hasil = query(query_str)
    # for data in hasil:
    #     data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'search_tayangan.html', {'tayangans': hasil})

def show_halaman_tayangan(request):
    if request.method == 'POST':
        id_tayangan = request.POST.get('id_tayangan')
    return redirect('show_film')
    
def show_film(request):
    if request.method == 'POST':
        id_film = request.POST.get('id_film')
    query_str = f"SELECT * FROM TAYANGAN JOIN FILM ON film.id_tayangan = tayangan.id WHERE id_tayangan = '{id_film}';"
    hasil = query(query_str)
    return render(request, 'film.html', {'films': hasil})

def show_series(request):
    if request.method == 'POST':
        id_series = request.POST.get('id_series')
    query_str = f"SELECT * FROM TAYANGAN JOIN SERIES ON series.id_tayangan = tayangan.id WHERE id_tayangan = '{id_series}';"
    hasil = query(query_str)
    return render(request, 'series.html', {'series': hasil})

def show_episode(request):
    query_str = "SELECT * FROM TAYANGAN JOIN SERIES ON series.id_tayangan = tayangan.id JOIN EPISODE ON episode.id_series = series.id_tayangan;"
    hasil = query(query_str)
    return render(request, 'episode.html', {'episode': hasil})