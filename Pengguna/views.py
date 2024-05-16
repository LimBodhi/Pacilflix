import random
from utils.query import connectdb
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import connection
from django.db.backends.utils import CursorWrapper

@connectdb
def register(cursor: CursorWrapper, request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        negara = request.POST.get('country')

        with connection.cursor() as cursor:
            # Cek apakah username sudah ada
            cursor.execute("SELECT * FROM pengguna WHERE username = %s", [username])
            users = cursor.fetchall()

            # Jika username sudah ada
            if len(users) > 0:
                messages.error(request, "Username yang Anda pilih sudah digunakan.")
                return render(request, 'register.html', {'form': request.POST})

            # Cek kekuatan password
            if len(password) < 8:
                messages.error(request, "Password minimal harus 8 karakter.")
                return render(request, 'register.html', {'form': request.POST})

            cursor.execute("SELECT id FROM TAYANGAN")
            shows = cursor.fetchall()
            random_show = str(random.choice(shows)[0])

            # Jika semua validasi terpenuhi
            cursor.execute("INSERT INTO PENGGUNA (username, password, id_tayangan, negara_asal) VALUES (%s, %s, %s, %s)", [username, password, random_show, negara])
            messages.success(request, 'Your account has been successfully created!')
            return redirect('LoginDanLogout:login')

    return render(request, 'register.html')