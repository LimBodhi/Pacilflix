from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from utils.query import query
from django.http import HttpResponseBadRequest, HttpResponseRedirect

# Function to show all favorite shows of a user
def show_favorit(request):
    username = request.session['username']
    query_str = f'''
                SELECT df.judul, df.timestamp, df.username 
                FROM daftar_favorit df 
                WHERE df.username = '{username}' 
                ORDER BY df.timestamp ASC;
                '''
    # Execute the query
    hasil = query(query_str)

    # Format the timestamp
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    
    return render(request, 'favorit.html', {'favorit': hasil})  

def remove_favorit(request):
    if request.method == 'POST':
        print("llla")
        judul = request.POST.get('judul')
        username = request.POST.get('username')
        query_str = f"DELETE FROM daftar_favorit WHERE judul = '{judul}' AND username = '{username}';"
        query(query_str)
    return redirect('show_favorit')

def remove_detail(request):
    print('masuk sini')
    if request.method == 'POST':
        print('masuk sini')
        timestamp = request.POST.get('timestamp')
        username = request.POST.get('username')
        id = request.POST.get('id_tayangan')
        query_str = f"DELETE FROM tayangan_memiliki_daftar_favorit WHERE timestamp = '{timestamp}' AND username = '{username}' AND id_tayangan = '{id}';"
        res=query(query_str)
        print(res)
    return redirect('show_favorit')

def show_favorit_detail(request, judul):
    username = request.session['username']
    query_str = f"""
        SELECT t.judul, t.id, tmdf.timestamp
        FROM tayangan t
        INNER JOIN tayangan_memiliki_daftar_favorit tmdf ON t.id = tmdf.id_tayangan
        INNER JOIN daftar_favorit df ON tmdf.timestamp = df.timestamp AND tmdf.username = df.username
        WHERE df.judul = '{judul}' AND df.username = '{username}';
    """
    result = query(query_str)
    if result:
        details = result[0]['judul']
        id = result[0]['id']
        timestamp = result[0]['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    else:
        details = ''
        id = ''
        timestamp = ''

    return render(request, 'favorit_detail.html', {'details': details, 'user': username, 'judul': judul, 'id': id, 'timestamp': timestamp})

def show_add_to_favorite(request):
    return render(request, 'add_to_favorite.html')
