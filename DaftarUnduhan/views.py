from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

#Fungsi untuk memanggil semua tayangan yang telah diunduh oleh user, dalam hal ini contohnya odavidson
def show_unduhan(request):
    query_str = '''
                select t.judul, tt.timestamp from tayangan t, tayangan_terunduh tt where t.id = tt.id_tayangan and tt.username = 'odavidson' order by tt.timestamp desc;
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