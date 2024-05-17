from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from utils.query import query
from datetime import datetime, timedelta

def show_unduhan(request):
    username = request.session['username']

    # Get the current date and time
    now = datetime.now()

    # Calculate the date and time for 7 days ago
    seven_days_ago = now - timedelta(days=7)

    # Construct the query string with the username and the date filter
    query_str = f'''
                SELECT t.judul, tt.timestamp 
                FROM tayangan t, tayangan_terunduh tt 
                WHERE t.id = tt.id_tayangan 
                AND tt.username = '{username}'
                AND tt.timestamp >= '{seven_days_ago.strftime("%Y-%m-%d %H:%M:%S")}'
                ORDER BY tt.timestamp DESC;
                '''

    # Execute the query
    hasil = query(query_str)

    # Format the timestamp
    for data in hasil:
        data['formatted_timestamp'] = data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    
    return render(request, 'index.html', {'unduhan': hasil})

from django.contrib import messages

def remove_unduhan(request):
    if request.method == 'POST':
        id_tayangan = request.POST.get('id_tayangan')
        username = request.user.username
        try:
            # Attempt to delete the unduhan
            query_str = f"DELETE FROM tayangan_terunduh WHERE id_tayangan = '{id_tayangan}' AND username = '{username}';"
            query(query_str)
            # If successful, display a success message
            messages.success(request, 'Tayangan berhasil dihapus dari daftar unduhan.')
        except Exception as e:
            # If unsuccessful, display an error message
            messages.error(request, f'Gagal menghapus tayangan dari daftar unduhan: {str(e)}')
    return redirect('show_unduhan')