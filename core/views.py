from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.db.models import Count

from .models import Post, Feedback, PostCategory, PostComment
from .forms import PostAddForm, PostCommentForm


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
    form = PostCommentForm()
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            PostComment.objects.create(title=form.cleaned_data['title'], post=post)
            return redirect('post_detail', post_id)

    return render(request, 'post_detail.html', {'post': post, 'form': form})


def post_add(request):

    post_form = PostAddForm()

    if request.method == 'POST':
        print(request.POST)
        # title = request.POST.get('title')
        # text = request.POST.get('text')
        # category = request.POST.get('category')
        # category = PostCategory.objects.get(id=category)

        # Post.objects.create(title=title, text=text, category=category)
        post_form = PostAddForm(request.POST, request.FILES)
        if post_form.is_valid():
            title = post_form.cleaned_data['title']
            text = post_form.cleaned_data['text']
            category = post_form.cleaned_data['category']
            image = post_form.cleaned_data['image']

            post = Post(title=title, text=text, category=category, image=image)
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
