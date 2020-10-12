from django.contrib.auth import login, logout, authenticate
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from mail.models import *

@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /wp-admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def home(request):
    return render(request, 'home.html')

def login_builtin_user(request):
    if request.method == 'POST':
        next = request.POST.get('next', None)
        if next and '://' in next:
            next = None
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect('home')
        else:
            return render(request, 'login.html', {'message': 'User not found or password invalid'})
    else:
        next = request.GET.get('next', None)
        if next and '://' in next:
            next = None
        return render(request, 'login.html', { 'next': next })

def logout_builtin_user(request):
    logout(request)
    return redirect('home')

# def signup(request):
#     if request.method == 'POST':
#         form = WIUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = WIUserCreationForm()
#     return render(request, 'signup.html', {'form': form})
