# Create your views here.

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from posts.form import PostForm, TestForm
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
        form = TestForm(request.POST, request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            Post.objects.create(
                title=cleaned_data["title"],
                content=cleaned_data["content"],
                rate=cleaned_data["rate"],
                image=cleaned_data["image"],
                category_id=cleaned_data["category"],
            )

            return redirect("posts")

        return render(request, "posts/create_post.html", context={"error": form.errors})

    form = PostForm()

    categories = Category.objects.all()

    return render(
        request,
        "posts/create_post.html",
        context={"form": form, "categories": categories},
    )


def edit_post(request: HttpRequest, pk):
    post = get_object_or_404(Post, id=pk)
    categories = Category.objects.all()
    if request.method == "POST":
        form = TestForm(request.POST, request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            post.title = cleaned_data["title"]
            post.content = cleaned_data["content"]
            post.rate = cleaned_data["rate"]
            if cleaned_data.get("image"):
                post.image = cleaned_data["image"]
            post.category_id = cleaned_data["category"]

            post.save()

            return redirect("post", id=post.pk)
        return render(
            request,
            "posts/edit_post.html",
            context={"post": post, "categories": categories, "errors": form.errors},
        )

    return render(
        request,
        "posts/edit_post.html",
        context={"post": post, "categories": categories},
    )


def delete_post(request: HttpRequest, id):

    if request.method == "GET":
        posts = get_object_or_404(Post, id=id)

        posts.delete()

        return redirect("posts")
