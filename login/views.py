from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")

    else:
        form = SignupForm()
    
    param = {
        'form': form
    }

    return render(request, 'login/signup.html', param)



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect("index")

    else:
        form = LoginForm()
    param = {
        'form': form,
    }
    return render(request, 'login/login.html', param)

def logout_view(request):
    logout(request)

    return redirect("index")






@login_required
def user_view(request):
    user = request.user

    params = {
        'user': user
    }

    return render(request, 'main/index.html', params)

@login_required
def other_view(request):
    users = User.objects.exclude(username=request.user.username)

    params = {
        'users': users
    }

    return render(request, 'login_app/other.html', params)
