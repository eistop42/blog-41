from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, get_user_model, authenticate, logout as auth_logout
from django.http import Http404
from .models import Profile, ProfileSubscription

from .forms import LoginForm, RegisterForm
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



def profile_subscribe(request, profile_id):
    profile = request.user.profile
    author = get_object_or_404(Profile, id=profile_id)
    if not author:
        raise Http404

    subs = ProfileSubscription.objects.filter(profile=profile, author=author).first()
    if subs:
        subs.delete()
    else:
        ProfileSubscription.objects.create(profile=profile, author=author)
    
    return redirect(request.GET['next'])
