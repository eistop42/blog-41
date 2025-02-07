from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.db.models import Count

from .models import Post, Feedback, PostCategory, PostComment
from .forms import LoginForm, PostAddForm, FeedbackForm, CommentAddForm, PostAddModelForm

def main(request):
    posts = Post.objects.all()

    category = request.GET.get('category')
    active_category = None

    if category:
        posts = posts.filter(category__id=category)
        active_category = PostCategory.objects.get(id=category)

    login_form = LoginForm()

    categories = PostCategory.objects.annotate(total_posts=Count('post'))

    return render(request, 'main.html', {'posts': posts,
                                         'categories': categories,
                                         'active_category': active_category,
                                         'login_form': login_form
                                         })


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentAddForm()

    if request.method == 'POST':

        form = CommentAddForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']

            post = Post.objects.get(id=post_id)
            PostComment.objects.create(title=title, post=post)

            return redirect('post_detail', post_id)

    return render(request, 'post_detail.html', {'post': post, 'form': form})


def post_add_old(request):
    error = ''
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title')
        text = request.POST.get('text')
        category = request.POST.get('category')
        category = PostCategory.objects.get(id=category)

        if title != '':

            Post.objects.create(title=title, text=text, category=category)

            return redirect('main')
        else:
            error = 'Ошибка. Пустой заголовок'

    categories = PostCategory.objects.all()

    return render(request, 'post_add.html', {'categories': categories, 'error': error})


def post_add(request):

    post_form = PostAddModelForm()

    if request.method == 'POST':
        # print(request.FILE)
        # print(request.FILES)
        print(request.FILES)
        print(request.POST)
        post_form = PostAddModelForm(request.POST, request.FILES)

        if post_form.is_valid():

            post_form.save()
            return redirect('main')

    return render(request, 'post_add.html', {'post_form': post_form})


def feedback(request):

    form = FeedbackForm()
    if request.method == 'POST':

        form = FeedbackForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['text']
            Feedback.objects.create(text=text)
            return redirect('feedback_success')

    return render(request, 'feedback.html', {'form': form} )


def feedback_success(request):
    return render(request, 'feedback_success.html', )
