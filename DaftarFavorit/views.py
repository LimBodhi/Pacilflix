from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

#Fungsi untuk memanggil semua tayangan favorit user, dalam hal ini contohnya pengguna0
def show_favorit(request):
    query_str = '''
                select df.judul, df.timestamp from daftar_favorit df where df.username = 'odavidson' order by df.timestamp ASC;
                '''
    # menjalankan query 
    hasil = query(query_str)

    # melakukan format waktu
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    
    return render(request, 'favorit.html', {'favorit': hasil})  


#Fungsi untuk menghapus tayangan yang telah difavoritkan oleh user
def remove_favorit(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        username = request.POST.get('username')
        query_str = f"DELETE FROM daftar_favorit WHERE judul = '{judul}' and username = '{username}';"
        query(query_str)
    return redirect('show_favorit')