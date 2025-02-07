from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

from .forms import LoginForm
def home(request):

    return render(request, 'profiles/home.html')


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            return redirect('profiles_home')

    return render(request, 'profiles/login.html', {'form': form})