from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import Post, Feedback, PostCategory

def main(request):

    posts = Post.objects.all()

    category = request.GET.get('category')

    if category:
        posts = posts.filter(category__id=category)

    categories = PostCategory.objects.all()

    return render(request, 'main.html', {'posts': posts, 'categories': categories})


def post_detail(request, post_id):

    post = Post.objects.get(id=post_id)

    return render(request, 'post_detail.html', {'post': post})


def post_add(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')

        Post.objects.create(title=title, text=text)

        return redirect('main')

    return render(request, 'post_add.html',)


def feedback(request):

    if request.method == 'POST':
        print(request.POST)

        text = request.POST.get('text')

        Feedback.objects.create(text=text)

        return redirect('feedback_success')

    return render(request, 'feedback.html',)

def feedback_success(request):

    return render(request, 'feedback_success.html', )