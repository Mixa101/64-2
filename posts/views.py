# Create your views here.
from django.shortcuts import get_object_or_404, render

from posts.models import Post
from posts.posts import get_posts_filter_by_rate


def home(request):
    return render(request, "base.html")


def post(request):
    posts = get_posts_filter_by_rate(2)
    return render(request, template_name="posts/posts.html", context={"posts": posts})


def get_post(request, id):
    post = get_object_or_404(Post, id=id)

    return render(request, template_name="posts/post.html", context={"post": post})


def get_posts_by_category(request, id):
    posts = Post.objects.filter(category_id=id)

    return render(request, template_name="posts/posts.html", context={"posts": posts})
