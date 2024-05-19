from django.http import JsonResponse
from django.shortcuts import render, redirect
from utils.query import query
from datetime import datetime, timedelta
from django.contrib import messages

def show_unduhan(request):
    username = request.session['username']

    # Get the current date and time
    now = datetime.now()

    # Calculate the date and time for 7 days ago
    seven_days_ago = now - timedelta(days=7)

    # Construct the query string with the username and the date filter
    query_str = f'''
                SELECT t.judul, tt.timestamp , tt.id_tayangan, tt.username
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

def remove_unduhan(request):
    if request.method == 'POST':
        id_tayangan = request.POST.get('id_tayangan')
        username = request.POST.get('username')

        # Check if the video has been added for more than 1 day
        try:
            query_str = f"SELECT timestamp FROM tayangan_terunduh WHERE id_tayangan = '{id_tayangan}' AND username = '{username}';"
            result = query(query_str)
            if result:
                timestamp = result[0]['timestamp']
                now = datetime.now()
                time_difference = now - timestamp
                if time_difference.days >= 1:
                    print('Video has been added for more than 1 day, proceed with deletion')
                    # Video has been added for more than 1 day, proceed with deletion
                    query(f"DELETE FROM tayangan_terunduh WHERE id_tayangan = '{id_tayangan}' AND username = '{username}';")
                else:
                    print('Tayangan tidak dapat dihapus karena belum diunduh selama lebih dari 1 hari.')
                    messages.error(request, 'Tayangan tidak dapat dihapus karena belum diunduh selama lebih dari 1 hari.')
            else:
                messages.error(request, 'Tayangan tidak ditemukan dalam daftar unduhan.')
        except Exception as e:
            messages.error(request, f'Gagal menghapus tayangan dari daftar unduhan: {str(e)}')

    return redirect('show_unduhan')