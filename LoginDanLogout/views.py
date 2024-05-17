# views.py
import datetime
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.backends.utils import CursorWrapper
from utils.query import connectdb

@connectdb
@csrf_exempt
def login(cursor: CursorWrapper, request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif len(username) < 3 or len(password) < 6:
            messages.error(request, 'Username must be at least 3 characters and password must be at least 6 characters.')

        if not messages.get_messages(request):
            cursor.execute("SELECT * FROM pengguna WHERE username = %s AND password = %s", [username, password])
            user = cursor.fetchone()

            if user:
                request.session['username'] = username
                request.session['is_logged_in'] = True
                response = HttpResponseRedirect(reverse("Tayangan:show_tayangan"))
                response.set_cookie('username', username)
                response.set_cookie('negara_asal', user[2])
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
            else:
                messages.error(request, 'Sorry, incorrect username or password. Please try again.')

    return render(request, 'login.html')

@csrf_exempt
def logout(request):
    response = HttpResponseRedirect(reverse('LoginDanLogout:show_main'))
    request.session.flush()
    response.delete_cookie('last_login')
    response.delete_cookie('username')
    response.delete_cookie('negara_asal')
    return response

def show_main(request):
    return render(request, "main.html")