from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, get_user_model, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Profile

from core.models import Post

from .forms import LoginForm, RegisterForm

@login_required
def home(request):

    # posts = Post.objects.fitler(profile=request.user.profile)
    posts = request.user.profile.profile_posts.all()

    print(posts)
    return render(request, 'profiles/home.html', {'posts': posts})


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            return redirect('profiles_home')

    return render(request, 'profiles/login.html', {'form': form})


def register(request):

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # создали пользователя
            User = get_user_model()
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            # создать Profile
            Profile.objects.create(user=user)

            # залогинить
            user = authenticate(request, username=username, password=password)
            auth_login(request, user)

            return redirect('profiles_home')

        # проверка валидности формы

    return render(request, 'profiles/register.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('main')