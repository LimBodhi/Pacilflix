from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from utils.query import query


def show_unduhan(request):
    username = request.session['username']

    # Construct the query string with the username
    query_str = f'''
                SELECT t.judul, tt.timestamp 
                FROM tayangan t, tayangan_terunduh tt 
                WHERE t.id = tt.id_tayangan 
                AND tt.username = '{username}' 
                ORDER BY tt.timestamp DESC;
                '''

    # Execute the query
    hasil = query(query_str)

    # Format the timestamp
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    
    return render(request, 'index.html', {'unduhan': hasil})

# Fungsi untuk menghapus tayangan yang telah diunduh oleh user
@login_required
def remove_unduhan(request):
    if request.method == 'POST':
        id_tayangan = request.POST.get('id_tayangan')
        username = request.user.username
        query_str = f"DELETE FROM tayangan_terunduh WHERE id_tayangan = '{id_tayangan}' AND username = '{username}';"
        query(query_str)
    return redirect('show_unduhan')
