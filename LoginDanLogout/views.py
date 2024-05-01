from django.shortcuts import redirect, render
from utils.query import query

def show_main(request):
    context = { "is_logged_in": False }

    if "username" in request.session:
        context["is_logged_in"] = True
        context["username"] = request.session["username"]

    return render(request, "main.html", context)

def login(request):
    context = {}
    if "username" in request.session:
        # TODO: Nanti ganti redirect jadi ke "Shows" (daftar tayangan)
        return redirect("LoginDanLogout:show_main")
    if "message" in request.session:
        context["message"] = request.session["message"]
        del request.session["message"]
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        data = query(
            "SELECT username, password FROM PENGGUNA WHERE username = %s AND password = %s", (username, password))
        if len(data) == 1:
            request.session["username"] = username
            # TODO: Nanti ganti redirect jadi ke "Shows" (daftar tayangan)
            return redirect("LoginDanLogout:show_main")
        else:
            context["message"] = "Login failed. Make sure you've inputted the correct credentials."
    return render(request, "login.html", context)

def logout(request):
    del request.session["username"]
    return redirect("LoginDanLogout:show_main")
