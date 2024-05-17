from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from utils.query import query
from django.http import HttpResponseBadRequest

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
        judul = request.POST.get('judul')
        username = request.POST.get('username')
        query_str = f"DELETE FROM daftar_favorit WHERE judul = '{judul}' AND username = '{username}';"
        query(query_str)
    return redirect('show_favorit')

# Function to show details of a specific favorite show
def show_favorit_detail(request, judul):
    username = request.session['username']
    query_str = f'''
                SELECT timestamp 
                FROM daftar_favorit df
                WHERE df.username = '{username}' AND df.judul = '{judul}';
                '''
    # Execute the query
    timestamp = query(query_str)

    query_str = f'''
                SELECT tm.id_tayangan 
                FROM tayangan_memiliki_daftar_favorit tm
                WHERE tm.username = '{username}' AND tm.timestamp = '{timestamp.pop()['timestamp']}';
                '''
    id_tayangan = query(query_str)

    query_str = f'''
                SELECT t.judul 
                FROM tayangan t
                WHERE t.id = '{id_tayangan.pop()['id_tayangan']}';
                '''
    hasil = query(query_str)

    return render(request, 'favorit_detail.html', {'details': hasil})