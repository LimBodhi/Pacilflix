import datetime
from utils.query import query
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# @login_required
def langganan_list(request):
    username = request.session['username']

    query_transaksi = f"""
        SELECT t.username, t.nama_paket, p.nama, p.harga, p.resolusi_layar, t.start_date_time, t.end_date_time, t.metode_pembayaran
        FROM PACILFLIX.TRANSACTION t
        JOIN PACILFLIX.PAKET p ON t.nama_paket = p.nama
        WHERE t.username = '{username}'
    """
    transaksi_data = query(query_transaksi)

    query_transaksi_aktif = f"""
        SELECT t.username, t.nama_paket, p.nama, p.harga, p.resolusi_layar, t.start_date_time, t.end_date_time, t.metode_pembayaran
        FROM PACILFLIX.TRANSACTION t
        JOIN PACILFLIX.PAKET p ON t.nama_paket = p.nama
        WHERE t.username = '{username}' AND t.end_date_time > NOW()
    """
    transaksi_data_aktif = query(query_transaksi_aktif)

    query_paket = "SELECT * FROM PACILFLIX.PAKET"
    paket_data = query(query_paket)
    
    dukungan_data = {}
    for paket in paket_data:
        nama_paket = paket['nama']
        query_dukungan = f"SELECT dukungan_perangkat FROM PACILFLIX.DUKUNGAN_PERANGKAT WHERE nama_paket = '{nama_paket}'"
        dukungan_data[nama_paket] = query(query_dukungan)
    
    for paket in paket_data:
        paket['dukungan_perangkat'] = [d['dukungan_perangkat'] for d in dukungan_data[paket['nama']]]
    
    for transaksi in transaksi_data:
        transaksi['dukungan_perangkat'] = [d['dukungan_perangkat'] for d in dukungan_data[transaksi['nama_paket']]]

    for transaksi in transaksi_data_aktif:
        transaksi['dukungan_perangkat'] = [d['dukungan_perangkat'] for d in dukungan_data[transaksi['nama_paket']]]
    
    # Pass the data to the template
    context = {
        'transaksi_data': transaksi_data,
        'transaksi_data_aktif': transaksi_data_aktif,
        'paket_data': paket_data
    }

    return render(request, 'langganan.html', context)

# @login_required
def beli_paket(request, nama_paket):
    query_str = f"SELECT * FROM PACILFLIX.PAKET WHERE nama = '{nama_paket}'"
    paket_data_list = query(query_str)
    
    query_dukungan = f"SELECT dukungan_perangkat FROM PACILFLIX.DUKUNGAN_PERANGKAT WHERE nama_paket = '{nama_paket}'"
    dukungan_data = query(query_dukungan)
    
    if paket_data_list and isinstance(paket_data_list, list):
        paket_data = paket_data_list[0]
        paket_data['dukungan_perangkat'] = [d['dukungan_perangkat'] for d in dukungan_data]
    else:
        paket_data = {}
    
    # Pass the data to the template
    context = {
        'paket': paket_data
    }
    return render(request, 'beli.html', context)

# @login_required
@csrf_exempt
def proses_pembayaran(request):
    if request.method == 'POST':
        username = request.session['username']
        nama_paket = request.POST.get('nama_paket') 
        metode_pembayaran = request.POST.get('metode_pembayaran') 
        timestamp_pembayaran = datetime.datetime.now()
        start_date_time = timestamp_pembayaran.date()
        end_date_time = (timestamp_pembayaran + datetime.timedelta(days=30)).date()
        
        query_str = f"""
                    INSERT INTO PACILFLIX.TRANSACTION (
                        username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran
                    ) VALUES (
                        '{username}', '{start_date_time}', '{end_date_time}', '{nama_paket}', '{metode_pembayaran}', '{timestamp_pembayaran}'
                    )
                    """
        result = query(query_str)

        return redirect('langganan_list')
