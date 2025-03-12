

from django.shortcuts import render, redirect, get_object_or_404

from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import Http404, JsonResponse
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Feedback, PostCategory, PostComment, PostLike
from .forms import LoginForm, PostAddForm, FeedbackForm, CommentAddForm, PostAddModelForm, PostFilterForm

def main(request):
    posts = Post.objects.all()

    page_number = request.GET.get('page', 1)

    active_category = None
    post_filter_form = PostFilterForm(request.GET)

    if post_filter_form.is_valid():
        category = post_filter_form.cleaned_data['category']
        order = post_filter_form.cleaned_data['order']

        if category:
            posts = posts.filter(category__in=category)

        if order == 'like_desc':
            posts = posts.annotate(likes=Count('post_likes', filter=Q(post_likes__is_liked=True)))
            posts = posts.order_by('-likes')
        if order == 'new':
            posts = posts.order_by('-created_date')
        if order == 'old':
            posts = posts.order_by('created_date')


    paginator = Paginator(posts, 1)
    page_obj = paginator.get_page(page_number)


    login_form = LoginForm()

    categories = PostCategory.objects.annotate(total_posts=Count('post'))

    return render(request, 'main.html', {'posts': posts,
                                         'categories': categories,
                                         'active_category': active_category,
                                         'login_form': login_form,
                                         'post_filter_form': post_filter_form,
                                         'page_obj': page_obj
                                         })

def post_search(request):

    text = request.GET.get('text')

    posts = Post.objects.filter(Q(text__icontains=text)|Q(title__icontains=text))

    return render(request, 'post_search.html', {'posts': posts, 'text': text})


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentAddForm()

    like = None

    likes = PostLike.objects.filter(post=post, is_liked=True).count()
    comments = PostComment.objects.filter(post=post).count()

    if request.user.is_authenticated:
        profile = request.user.profile
        like = PostLike.objects.filter(post=post, profile=profile).first()

    if request.method == 'POST':

        form = CommentAddForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            title = form.cleaned_data['title']

            post = Post.objects.get(id=post_id)
            comment = PostComment.objects.create(title=title, post=post)
            comment.profile = request.user.profile
            comment.save()

            comments_count = PostComment.objects.filter(post=post).count()

            comments = render_to_string('parts/comment.html', {"post":post, 'comments': comments_count }, request )
            form = render_to_string('parts/comment_form.html', {'form': CommentAddForm(), 'post': post}, request)

            return JsonResponse({'comments': comments, 'is_valid': True, 'form': form })

        if not form.is_valid():
            form = render_to_string('parts/comment_form.html', {'form': form, 'post': post}, request)

            return JsonResponse({'form': form, 'is_valid': False})

    return render(request, 'post_detail.html', {'post': post, 'form': form, 'like': like, 'likes': likes, "comments": comments})


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

            return redirect('main')

    return render(request, 'post_add.html', {'post_form': post_form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not Post.objects.filter(profile=request.user.profile, id=post_id).exists():
        raise Http404

    post_form = PostAddModelForm(instance=post)

    if request.method == 'POST':
        post_form = PostAddModelForm(request.POST, request.FILES, instance=post)

        if post_form.is_valid():
            post_form.save()
            return redirect('post_detail', post.id)

    return render(request, 'post_edit.html', {'post_form': post_form})


@login_required
def post_delete(request, post_id):

    if not Post.objects.filter(profile=request.user.profile, id=post_id).exists():
        raise Http404

    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('main')


def feedback(request):

    form = FeedbackForm()
    if request.method == 'POST':

        form = FeedbackForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['text']
            Feedback.objects.create(text=text)
            return redirect('feedback_success')

    return render(request, 'feedback.html', {'form': form} )

class FeedbackView(View):


    def get_form(self):
        return FeedbackForm()

    def get(self, request):
        form = self.get_form()
        return render(request, 'feedback.html', {'form': form})

    def post(self, request):
        form = FeedbackForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['text']
            Feedback.objects.create(text=text)
            return redirect('feedback_success')

        return render(request, 'feedback.html', {'form': form})

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
        PostLike.objects.create(post=post, profile=user.profile)

    likes = PostLike.objects.filter(post=post, is_liked=True).count()

    return JsonResponse({'likes': likes})


@login_required
def post_unlike(request, post_id):

    user = request.user
    post = Post.objects.get(id=post_id)

    post_like = PostLike.objects.filter(post=post, profile=user.profile).first()

    if post_like:
        post_like.is_liked = False
        post_like.save()

    likes = PostLike.objects.filter(post=post, is_liked=True).count()

    return JsonResponse({'likes': likes})


@login_required
def comment_delete(request, post_id, comment_id):
    profile = request.user.profile

    if not PostComment.objects.filter(profile=profile, id=comment_id).exists():
        raise Http404

    PostComment.objects.filter(profile=profile, id=comment_id).delete()

    return redirect('post_detail', post_id)


def test(request):

    return render(request, 'test.html', )

class TestView(TemplateView):
    template_name = 'test.html'

    def get_context_data(self):
        return {'name': 'ilya'}

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['text', 'title', 'category']
    template_name = 'post_create_view.html'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save()

        self.object.profile = self.request.user.profile
        self.object.save()

        return redirect(self.success_url)
