import datetime
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

def langganan_list(request):
    # Query untuk mendapatkan data paket langganan dan transaksi untuk odavidson
    query_transaksi = """
    SELECT t.username, t.nama_paket, p.nama, p.harga, p.resolusi_layar, t.start_date_time, t.end_date_time, t.metode_pembayaran
    FROM PACILFLIX.TRANSACTION t
    JOIN PACILFLIX.PAKET p ON t.nama_paket = p.nama
    WHERE t.username = 'odavidson'
    """
    transaksi_data = query(query_transaksi)
    
    # Query untuk mendapatkan data paket langganan
    query_paket = "SELECT * FROM PACILFLIX.PAKET"
    paket_data = query(query_paket)
    
    # Query untuk mendapatkan dukungan perangkat untuk setiap paket
    dukungan_data = {}
    for paket in paket_data:
        nama_paket = paket['nama']
        query_dukungan = f"SELECT dukungan_perangkat FROM PACILFLIX.DUKUNGAN_PERANGKAT WHERE nama_paket = '{nama_paket}'"
        dukungan_data[nama_paket] = query(query_dukungan)
    
    # Tambahkan dukungan perangkat ke paket_data
    for paket in paket_data:
        paket['dukungan_perangkat'] = [d['dukungan_perangkat'] for d in dukungan_data[paket['nama']]]
    
    # Tambahkan dukungan perangkat ke transaksi_data
    for transaksi in transaksi_data:
        transaksi['dukungan_perangkat'] = [d['dukungan_perangkat'] for d in dukungan_data[transaksi['nama_paket']]]
    
    # Pass the data to the template
    context = {
        'transaksi_data': transaksi_data,
        'paket_data': paket_data
    }
    return render(request, 'langganan.html', context)

def beli_paket(request, nama_paket):
    # Query to get the details of the package the user wants to purchase
    query_str = f"SELECT * FROM PACILFLIX.PAKET WHERE nama = '{nama_paket}'"
    paket_data_list = query(query_str)
    
    # Query to get the supported devices for the package
    query_dukungan = f"SELECT dukungan_perangkat FROM PACILFLIX.DUKUNGAN_PERANGKAT WHERE nama_paket = '{nama_paket}'"
    dukungan_data = query(query_dukungan)
    
    # Check if paket_data_list is not empty and is a list
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

@csrf_exempt
def proses_pembayaran(request):
    if request.method == 'POST':
        # Ambil data dari form
        username = 'odavidson'
        # username = request.POST.get('username')  # asumsikan form memiliki field 'username'
        nama_paket = request.POST.get('nama_paket')  # asumsikan form memiliki field 'nama_paket'
        metode_pembayaran = request.POST.get('metode_pembayaran')  # asumsikan form memiliki field 'metode_pembayaran'
        
        # Tentukan tanggal dan waktu pembayaran saat ini
        timestamp_pembayaran = datetime.datetime.now()
        
        # Tentukan tanggal mulai dan akhir berlangganan (misalnya 1 bulan dari tanggal pembayaran)
        start_date_time = timestamp_pembayaran.date()
        end_date_time = (timestamp_pembayaran + datetime.timedelta(days=30)).date()
        
        # Masukkan data transaksi ke dalam database
        query_str = f"""
        INSERT INTO PACILFLIX.TRANSACTION (
            username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran
        ) VALUES (
            '{username}', '{start_date_time}', '{end_date_time}', '{nama_paket}', '{metode_pembayaran}', '{timestamp_pembayaran}'
        )
        """
        result = query(query_str)
        
        # Periksa apakah query berhasil
        if isinstance(result, Exception):
            # Jika terjadi kesalahan, kembalikan pesan error
            return JsonResponse({'status': 'error', 'message': str(result)}, status=500)
        
        # Jika berhasil, kembalikan respons sukses
        return JsonResponse({'status': 'success', 'message': 'Pembayaran berhasil'})
    else:
        # Jika metode request bukan POST, kembalikan error
        return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, status=405)