from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from profiles.models import ProfileSubscription

from .models import Post, Feedback, PostCategory, PostComment, PostLike
from .forms import LoginForm, PostAddForm, FeedbackForm, CommentAddForm, PostAddModelForm, PostFilterForm



def main(request):
    posts = Post.objects.all()

    category = request.GET.get('category')
    active_category = None

    post_filter = PostFilterForm(request.GET)

    if post_filter.is_valid():
        posts = posts.annotate(likes=Count('post_likes'))
        posts = posts.annotate(comments=Count('post_comments'))

        data = post_filter.cleaned_data
        order = data['order']
        category = data['category']

        if category:
            posts = posts.filter(category__in=data['category'])

        if order == 'like_desc':
            posts = posts.order_by('-likes')
        elif order == 'like_asc':
            posts = posts.order_by('likes')
        elif order == 'comment_desc':
            posts = posts.order_by('-comments')


    # if category:
    #     posts = posts.filter(category__id=category)
    #     active_category = PostCategory.objects.get(id=category)

    login_form = LoginForm()

    categories = PostCategory.objects.annotate(total_posts=Count('post'))


    return render(request, 'main.html', {'posts': posts,
                                         'categories': categories,
                                         'active_category': active_category,
                                         'login_form': login_form,
                                         'post_filter': post_filter
                                         })


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentAddForm()

    like = None
    sub = None


    likes = PostLike.objects.filter(post=post, is_liked=True).count()
    comments = PostComment.objects.filter(post=post).count()
    if request.user.is_authenticated:
        profile = request.user.profile
        like = PostLike.objects.filter(post=post, profile=profile).first()
        sub = ProfileSubscription.objects.filter(profile=profile, author=post.profile).first()

    if request.method == 'POST':

        form = CommentAddForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            title = form.cleaned_data['title']

            post = Post.objects.get(id=post_id)
            comment = PostComment.objects.create(title=title, post=post)
            comment.profile = request.user.profile
            comment.save()

            comment = render_to_string( 'parts/comment.html', {'comment': comment})

            return JsonResponse({'comment': comment})
        else:
            errors = render_to_string( 'parts/comment_form_errors.html', {'form': form})
            return JsonResponse({"errors": errors}, status=400)

    return render(request, 'post_detail.html', {'post': post, 
    'form': form, 'like': like, 'likes': likes, "comments": comments, 'sub': sub})


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


@login_required
def post_add(request):

    post_form = PostAddModelForm()

    if request.method == 'POST':
        # print(request.FILE)
        # print(request.FILES)
        print(request.FILES)
        print(request.POST)
        post_form = PostAddModelForm(request.POST, request.FILES)

        if post_form.is_valid():

            post = post_form.save(commit=False)
            post.profile = request.user.profile
            post.save()

            return render(request, 'parts/post_add_success.html')

        return render(request, 'parts/post_add_form.html', {'post_form': post_form})

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


@login_required
def post_like(request, post_id):

    user = request.user
    post = Post.objects.get(id=post_id)

    post_like = PostLike.objects.filter(post=post, profile=user.profile).first()
    if post_like:
        post_like.is_liked = True
        post_like.save()
    else:
        post_like = PostLike.objects.create(post=post, profile=user.profile)

    likes =  PostLike.objects.filter(post=post, is_liked=True).count()

    return JsonResponse({'likes': likes, 'post_like': post_like.is_liked})


@login_required
def post_unlike(request, post_id):

    user = request.user
    post = Post.objects.get(id=post_id)

    post_like = PostLike.objects.filter(post=post, profile=user.profile).first()

    if post_like:
        post_like.is_liked = False
        post_like.save()
    
    likes =  PostLike.objects.filter(post=post, is_liked=True).count()

    return JsonResponse({'likes': likes, 'post_like': post_like.is_liked})


@login_required
def comment_delete(request, post_id, comment_id):
    profile = request.user.profile

    PostComment.objects.filter(profile=profile, id=comment_id).delete()

    return redirect('post_detail', post_id)