from django.shortcuts import redirect, render
from utils.query import query
import random

def register(request):
    if "username" in request.session:
        # TODO: Ganti redirect jadi ke "Shows" (daftar tayangan)
        return redirect("main:show_main")
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        negara_asal = request.POST.get("country")

        random_show = str(random.choice(query("SELECT id FROM tayangan"))["id"])

        exists = query(
            "SELECT * FROM PENGGUNA WHERE username = %s", (username,))
        if len(exists) > 0:
            context["message"] = "Username already taken. Please choose another username."
        else:
            data = query("INSERT INTO PENGGUNA (username, password, id_tayangan, negara_asal) VALUES (%s,%s,%s,%s)",
                         (username, password, random_show, negara_asal))
            request.session["message"] = "Account creation successful! You can log in now."
            return redirect("authentication:login")
    return render(request, "register.html", context)