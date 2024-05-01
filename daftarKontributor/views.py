from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

def show_kontributor(request):
    tipe_kontributor = request.GET.get('tipe', None)
    query_str = """
        SELECT c.nama, c.jenis_kelamin, c.kewarganegaraan, 
        CASE 
            WHEN s.id IS NOT NULL THEN 'Sutradara'
            WHEN p.id IS NOT NULL THEN 'Pemain'
            WHEN ps.id IS NOT NULL THEN 'Penulis Skenario'
            ELSE 'Tidak Diketahui'
        END as tipe
        FROM CONTRIBUTORS c
        LEFT JOIN SUTRADARA s ON c.id = s.id
        LEFT JOIN PEMAIN p ON c.id = p.id
        LEFT JOIN PENULIS_SKENARIO ps ON c.id = ps.id
    """
    if tipe_kontributor:
        # Menambahkan filter WHERE sesuai dengan tipe kontributor
        query_str += f" WHERE '{tipe_kontributor}' = CASE WHEN s.id IS NOT NULL THEN 'Sutradara' WHEN p.id IS NOT NULL THEN 'Pemain' WHEN ps.id IS NOT NULL THEN 'Penulis Skenario' END"
    query_str += " ORDER BY c.nama ASC;"
    hasil = query(query_str)
    return render(request, 'kontributor.html', {'kontributors': hasil})