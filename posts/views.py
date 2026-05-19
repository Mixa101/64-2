# Create your views here.


from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from posts.form import PostForm
from posts.models import Category, Post
from posts.posts import get_categories, get_posts_filter_by_rate

# CBV - Class Based Views


def home(request):
    return render(request, "base.html")


class GetPostListView(ListView):
    template_name = "posts/posts.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 6

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return context

    def get_queryset(self) -> QuerySet[Any]:
        queryset = get_posts_filter_by_rate(2)

        count = queryset.count()

        print(count)

        return queryset


class PostDetailView(DetailView):
    template_name = "posts/post.html"
    model = Post
    context_object_name = "post"


# def get_post(request, id):
#     post = get_object_or_404(Post, id=id)

#     return render(request, template_name="posts/post.html", context={"post": post})


def get_posts_by_category(request, id):
    category = Category.objects.filter(id=id).first()

    posts = category.posts.all()

    return render(
        request,
        template_name="posts/posts.html",
        context={"posts": posts, "category": category},
    )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/create_post.html"
    form_class = PostForm
    success_url = reverse_lazy("posts")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = get_categories()
        return context


# @login_required
# def create_post(request: HttpRequest):

#     if request.method == "POST":
#         form = TestForm(request.POST, request.FILES)

#         if form.is_valid():
#             cleaned_data = form.cleaned_data

#             tags = form.cleaned_data["tags"].split(" ")
#             tag_objects = []
#             for tag in tags:
#                 tag_objects.append(Tag(title=tag))

#             if tag_objects:
#                 Tag.objects.bulk_create(tag_objects)

#             Post.objects.create(
#                 title=cleaned_data["title"],
#                 content=cleaned_data["content"],
#                 rate=cleaned_data["rate"],
#                 image=cleaned_data["image"],
#                 category_id=cleaned_data["category"],
#                 user=request.user,
#             )

#             return redirect("posts")

#         return render(request, "posts/create_post.html", context={"error": form.errors})

#     form = PostForm()

#     categories = Category.objects.all()

#     return render(
#         request,
#         "posts/create_post.html",
#         context={"form": form, "categories": categories},
#     )


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
