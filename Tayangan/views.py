from django.db import connection
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

def show_tayangan(request):
    query_str = """SELECT generate_series(1, 10) AS peringkat, 
                        t.judul, 
                        t.sinopsis_trailer, 
                        t.url_video_trailer, 
                        t.release_date_trailer, 
                        generate_series(1, 10) AS total_view, t.id FROM TAYANGAN t LIMIT 10;"""
    hasil = query(query_str)

    query_str_film = "SELECT * FROM TAYANGAN JOIN FILM ON film.id_tayangan = tayangan.id;"
    hasil_film = query(query_str_film)
    query_str_series = "SELECT * FROM TAYANGAN JOIN SERIES ON series.id_tayangan = tayangan.id;"
    hasil_series = query(query_str_series)

    return render(request, 'tayangan.html', {'tayangans': hasil, 'tayangan_film': hasil_film, 'tayangan_series': hasil_series})

def show_search_tayangan(request):
    if request.method == 'GET':
        search_query = request.GET.get('search')
    query_str = f" SELECT tayangan.judul, tayangan.sinopsis_trailer, tayangan.url_video_trailer, tayangan.release_date_trailer FROM TAYANGAN WHERE tayangan.judul LIKE '%{search_query}%';"
    hasil = query(query_str)

    return render(request, 'search_tayangan.html', {'tayangans': hasil})

def show_halaman_tayangan(request):
    if request.method == 'POST':
        id_tayangan = request.POST.get('id_tayangan')
    with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM film WHERE id_tayangan = %s", [id_tayangan])
            film_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM episode WHERE id_series = %s", [id_tayangan])
            episode_count = cursor.fetchone()[0]
    if film_count > 0:
        return redirect('Tayangan:show_film', id_film=id_tayangan)
    elif episode_count > 0:
        return redirect('Tayangan:show_series', id_series=id_tayangan)
    else:
        return redirect('page_not_found')
    
def show_film(request):
    if request.method == 'POST':
        id_film = request.POST.get('id_film')

    query_str = f"""
    SELECT 
        t.judul, 
        COUNT(*) AS total_view, 
        ROUND(AVG(u.rating), 2) AS rata_rata_rating, 
        t.sinopsis, 
        f.durasi_film, 
        f.release_date_film, 
        f.url_video_film, 
        ARRAY_AGG(DISTINCT gt.genre) AS genres, 
        t.asal_negara, 
        ARRAY_AGG(DISTINCT cp.nama) AS pemains, 
        ARRAY_AGG(DISTINCT cps.nama) AS penulis_skenario, 
        cs.nama AS sutradara
        f.id_tayangan
    FROM 
        TAYANGAN t 
    JOIN 
        FILM f ON f.id_tayangan = t.id 
    LEFT JOIN 
        RIWAYAT_NONTON rn ON rn.id_tayangan = t.id 
    LEFT JOIN 
        ULASAN u ON u.id_tayangan = t.id 
    LEFT JOIN 
        GENRE_TAYANGAN gt ON gt.id_tayangan = t.id 
    LEFT JOIN 
        MEMAINKAN_TAYANGAN mt ON mt.id_tayangan = t.id 
    LEFT JOIN 
        MENULIS_SKENARIO_TAYANGAN mst ON mst.id_tayangan = t.id 
    LEFT JOIN 
        CONTRIBUTORS cp ON cp.id = mt.id_pemain 
    LEFT JOIN 
        CONTRIBUTORS cps ON cps.id = mst.id_penulis_skenario 
    LEFT JOIN 
        CONTRIBUTORS cs ON cs.id = t.id_sutradara 
    WHERE 
        t.id = '{id_film}' 
    AND 
        EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) >= 0.7 * (
            CASE 
                WHEN f.id_tayangan IS NOT NULL THEN f.durasi_film * 60 
                ELSE 0 
            END
        )
    GROUP BY 
        t.judul, t.sinopsis, f.durasi_film, f.release_date_film, f.url_video_film, t.asal_negara, cs.nama;
    """

    hasil = query(query_str)
    query_str_ulasan = ''' SELECT ulasan.username, ulasan.deskripsi, ulasan.rating, ulasan.timestamp 
                    FROM ULASAN 
                    JOIN TAYANGAN ON tayangan.id = ulasan.id_tayangan
                    ORDER BY ulasan.timestamp DESC;
                '''
    hasil_ulasan = query(query_str_ulasan)
    for data in hasil_ulasan:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")

    return render(request, 'film.html', {'films': hasil, 'ulasans':hasil_ulasan})

def show_series(request):
    if request.method == 'POST':
        id_series = request.POST.get('id_series')
    
    query_str = f"""
    SELECT 
        t.judul, 
        ARRAY_AGG(DISTINCT e.url_video) AS episodes, 
        COUNT(*) AS total_view, 
        ROUND(AVG(u.rating), 2) AS rata_rata_rating, 
        t.sinopsis, 
        ARRAY_AGG(DISTINCT gt.genre) AS genres, 
        t.asal_negara, 
        ARRAY_AGG(DISTINCT cp.nama) AS pemains, 
        ARRAY_AGG(DISTINCT cps.nama) AS penulis_skenario, 
        cs.nama AS sutradara
    FROM 
        TAYANGAN t 
    JOIN 
        SERIES s ON s.id_tayangan = t.id 
    LEFT JOIN 
        EPISODE e ON e.id_series = s.id_tayangan 
    LEFT JOIN 
        RIWAYAT_NONTON rn ON rn.id_tayangan = t.id 
    LEFT JOIN 
        ULASAN u ON u.id_tayangan = t.id 
    LEFT JOIN 
        GENRE_TAYANGAN gt ON gt.id_tayangan = t.id 
    LEFT JOIN 
        MEMAINKAN_TAYANGAN mt ON mt.id_tayangan = t.id 
    LEFT JOIN 
        MENULIS_SKENARIO_TAYANGAN mst ON mst.id_tayangan = t.id 
    LEFT JOIN 
        CONTRIBUTORS cp ON cp.id = mt.id_pemain 
    LEFT JOIN 
        CONTRIBUTORS cps ON cps.id = mst.id_penulis_skenario 
    LEFT JOIN 
        CONTRIBUTORS cs ON cs.id = t.id_sutradara 
    WHERE 
        s.id_tayangan = '{id_series}'
    AND 
        EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) >= 0.7 * (
            CASE 
                WHEN s.id_tayangan IS NOT NULL THEN SUM(e.durasi) * 60 
                ELSE 0 
            END
        )
    GROUP BY 
        t.judul, t.sinopsis, t.asal_negara, cs.nama, total_view;
    """
    
    hasil = query(query_str)
    # for data in hasil:
    #     data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'series.html', {'series': hasil})

def show_episode(request):
    if request.method == 'POST':
        sub_judul = request.POST.get('sub_judul')
    query_str = f" SELECT t.judul, e1.sub_judul, ARRAY_AGG(e.url_video), e1.sinopsis, e1.durasi, e1.url_video, e1.release_date FROM TAYANGAN t JOIN SERIES s ON s.id_tayangan = t.id JOIN EPISODE e ON e.id_series = s.id_tayangan JOIN EPISODE e1 ON e1.sub_judul = '{sub_judul}';"
    hasil = query(query_str)
    # for data in hasil:
    #     data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'episode.html', {'episode': hasil})