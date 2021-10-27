from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def create_user(request):
    if request.user.is_authenticated:
        return redirect('veriuser:home')
    else:
        context = {}
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account Successfully created for ' + user )
                return redirect('veriuser:login')
            else:
                context['form'] = form
                context['error'] ='invalid input'
                return render(request, "create_user.html", context)
        else:
            form = CreateUserForm()
        context['form'] = form
        return render(request, "create_user.html", context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('library:home')
    else:
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('library:home')
            else:
                context = {}
                context['form'] = UserLoginForm()
                messages.info(request, 'username or password is incorrect')
                return render(request, "login.html", context)

        context = {}
        context['form']=UserLoginForm()
        return render(request, "login.html", context)

def logout_user(request):
    logout(request,)
    return redirect('veriuser:login')