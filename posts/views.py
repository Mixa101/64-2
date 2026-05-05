# Create your views here.
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostForm
from posts.models import Category, Post
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


def create_post(request: HttpRequest):

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("posts")

        return render(request, "posts/create_post.html", context={"error": form.errors})

        # title = request.POST.get("title", "").strip()
        # content = request.POST.get("content", "")
        # rate = request.POST.get("rate", 0)
        # image = request.FILES.get("image")

        # banned_words = ["plohoe slovo", "ban", "INSERT", "SELECT"]

        # if title in banned_words:
        #     return render(
        #         request,
        #         "posts/create_post.html",
        #         context={
        #             "error": "Нельзя создать пост с таким названием!",
        #             "title": title,
        #             "content": content,
        #             "rate": rate,
        #             "image": image,
        #         },
        #     )

        # if not title or not content or not rate:
        #     return render(
        #         request,
        #         "posts/create_post.html",
        #         context={
        #             "error": "Нельзя создать пустой пост!",
        #             "title": title,
        #             "content": content,
        #             "rate": rate,
        #             "image": image,
        #         },
        #     )
        # Post.objects.create(title=title, content=content, rate=rate, image=image)

    form = PostForm()

    categories = Category.objects.all()

    return render(
        request,
        "posts/create_post.html",
        context={"form": form, "categories": categories},
    )
