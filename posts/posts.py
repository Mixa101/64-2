from posts.models import Category, Post


def get_posts_filter_by_rate(rate):

    posts = Post.objects.filter(rate__gt=rate).order_by("-created_at")

    return posts


def get_all_posts():
    posts = Post.objects.all()

    return posts


def get_categories():
    return Category.objects.all()
