from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# view for signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:signup")

        try:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect("home")
        except:
            messages.error(request, "Username already taken.")
            return redirect("accounts:signup")

    return render(request, "accounts/signup.html")

# view for login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")

# view for logout
def logout_view(request):
    logout(request)
    return redirect("home")
