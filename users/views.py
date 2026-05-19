# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView


def login_user(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "users/login.html")


def logout_user(request):

    logout(request)

    return redirect("home")


class CreateUserView(CreateView):
    template_name = "users/register.html"
    fields = ("username", "password")
    model = User
    success_url = reverse_lazy("home")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.password = make_password(self.request.POST.get("password"))

        return super().form_valid(form)
