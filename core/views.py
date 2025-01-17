from django.shortcuts import render

from django.http import HttpResponse

from .models import Post

def main(request):

    posts = Post.objects.all()

    return render(request, 'main.html', {'posts': posts})


def post_detail(request, post_id):

    post = Post.objects.get(id=post_id)

    return render(request, 'post_detail.html', {'post': post})
