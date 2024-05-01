from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

#Fungsi untuk memanggil semua tayangan yang telah diunduh oleh user, dalam hal ini contohnya pengguna0
def show_unduhan(request):
    query_str = '''SELECT tayangan.judul, tayangan_terunduh.timestamp, tayangan_terunduh.id_tayangan 
                    FROM tayangan
                    JOIN tayangan_terunduh ON tayangan.id = tayangan_terunduh.id_tayangan
                    WHERE tayangan_terunduh.username = 'pengguna0'
                    ORDER BY tayangan_terunduh.timestamp ASC;
                '''
    #menjakankan query 
    hasil = query(query_str)
    
    #melakukan format waktu
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    
    return render(request, 'index.html', {'unduhan': hasil})

#Fungsi untuk menghapus tayangan yang telah diunduh oleh user
def remove_unduhan(request):
    if request.method == 'POST':
        id_tayangan = request.POST.get('id_tayangan')
        query_str = f"DELETE FROM tayangan_terunduh WHERE id_tayangan = '{id_tayangan}';"
        query(query_str)
    return redirect('show_unduhan')