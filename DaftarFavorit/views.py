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
        judul = request.POST.get('judul')
        username = request.POST.get('username')
        query_str = f"DELETE FROM daftar_favorit WHERE judul = '{judul}' AND username = '{username}';"
        query(query_str)
    return redirect('show_favorit')

def show_favorit_detail(request, judul):
    if request.method == 'POST':
        return redirect('delete_detail')
    username = request.session['username']
    timestamp_query_str = f"""
                SELECT timestamp 
                FROM daftar_favorit df
                WHERE df.username = '{username}' AND df.judul = '{judul}';
                """
    timestamp_result = query(timestamp_query_str)
    
    if isinstance(timestamp_result, list) and len(timestamp_result) > 0:
        timestamp = timestamp_result.pop()['timestamp']
        
    else:
        timestamp = ''  

    id_tayangan_query_str = f"""
                SELECT tm.id_tayangan 
                FROM tayangan_memiliki_daftar_favorit tm
                WHERE tm.username = '{username}' AND tm.timestamp = '{timestamp}';
                """
    id_tayangan_result = query(id_tayangan_query_str)
    
    if isinstance(id_tayangan_result, list) and len(id_tayangan_result) > 0:
        id_tayangan = id_tayangan_result.pop()['id_tayangan']
    else:
        id_tayangan = ''  

    details_query_str = f"""
                SELECT t.judul 
                FROM tayangan t
                WHERE t.id = '{id_tayangan}';
                """
    details_result = query(details_query_str)
    
    if isinstance(details_result, list) and len(details_result) > 0:
        details = details_result.pop()['judul']
    else:
        details = ''  

    return render(request, 'favorit_detail.html', {'details': details, 'timestamp': timestamp, 'id_tayangan': id_tayangan, 'user':request.session['username'], 'judul':judul})

def delete_detail_favorit(request):
    timestamp = request.POST.get('timestamp')
    id_tayangan = request.POST.get('id_tayangan')
    username = request.POST.get('username')

    query_str = f"DELETE FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT WHERE id_tayangan='{id_tayangan}' AND timestamp='{timestamp}' AND username = '{username}'"
    query(query_str, return_result=False)
    return redirect(show_favorit_detail)
