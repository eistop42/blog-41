from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.db.models import Count

from .models import Post, Feedback, PostCategory
from .forms import PostAddForm


def main(request):
    posts = Post.objects.all()

    category = request.GET.get('category')
    active_category = None

    if category:
        posts = posts.filter(category__id=category)
        active_category = PostCategory.objects.get(id=category)

    categories = PostCategory.objects.annotate(total_posts=Count('post'))


    return render(request, 'main.html', {'posts': posts,
                                         'categories': categories,
                                         'active_category': active_category
                                         })


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)

    return render(request, 'post_detail.html', {'post': post})


def post_add(request):

    post_form = PostAddForm()

    if request.method == 'POST':
        print(request.POST)
        # title = request.POST.get('title')
        # text = request.POST.get('text')
        # category = request.POST.get('category')
        # category = PostCategory.objects.get(id=category)

        # Post.objects.create(title=title, text=text, category=category)
        post_form = PostAddForm(request.POST)
        if post_form.is_valid():
            title = post_form.cleaned_data['title']
            text = post_form.cleaned_data['text']
            category = post_form.cleaned_data['category']

            post = Post(title=title, text=text, category=category)
            post.save()

            return redirect('main')

    categories = PostCategory.objects.all()


    return render(request, 'post_add.html', {'categories': categories, 'form': post_form})


def feedback(request):
    if request.method == 'POST':
        print(request.POST)

        text = request.POST.get('text')

        Feedback.objects.create(text=text)

        return redirect('feedback_success')

    return render(request, 'feedback.html', )


def feedback_success(request):
    return render(request, 'feedback_success.html', )
