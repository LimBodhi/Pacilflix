import datetime
from utils.query import connectdb
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.backends.utils import CursorWrapper
from django.http import HttpResponseRedirect

@connectdb
def login(cursor: CursorWrapper, request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cursor.execute(f"SELECT username, password FROM PENGGUNA WHERE username = '{username}' AND password = '{password}'")
        user = cursor.fetchone()

        if user:
            request.session['username'] = username
            request.session['is_logged_in'] = True
            response = HttpResponseRedirect(reverse('Tayangan:show_tayangan'))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'Sorry, incorrect username or password. Please try again.')

    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('LoginDanLogout:show_main'))

def show_main(request):
    context = { "is_logged_in": False }

    if "username" in request.session:
        context["is_logged_in"] = True
        context["username"] = request.session["username"]

    return render(request, "main.html", context)