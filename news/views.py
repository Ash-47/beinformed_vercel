from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import requests
from django.shortcuts import render, redirect, reverse
from .models import *
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


# Create your views here.
testjson = []
searcharts = []
flag = 0
q = None


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            print("authenticated")
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            print("nop")
            return render(
                request,
                "news/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "news/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "news/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "news/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "news/register.html")


@cache_page(1800)
def home(request):
    # global flag
    # global testjson
    # print(flag)
    # print("test message")
    if request.user.is_authenticated:
        stuff = [cat.category for cat in request.user.following.all()]
    else:
        stuff = []
    # print(request.session.get("flag"))
    # if request.session.get("flag", 0) < 1:
    #     # print(settings.API_KEY)
    response = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={settings.API_KEY}"
    )
    print(response.status_code)
    request.session["flag"] = 1
    if response.json()["status"] != "ok":
        return render(
            request,
            "news/home.html",
            {
                "articles": None,
                "stuff": stuff,
                "code": response.json()["code"],
                "message": response.json()["message"],
            },
        )
        # else:
        #     flag += 1
        #     # print("inside else")
        #     testjson = response.json()["articles"]
    paginator = Paginator(response.json()["articles"], 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # request.session.set_expiry(300)
    # print(testjson)
    #  print(page_obj)
    return render(request, "news/home.html", {"articles": page_obj, "stuff": stuff})


def housekeeping(arts, name):
    global searcharts
    global q
    searcharts = arts
    q = name


# @csrf_exempt
def search(request):
    global searcharts
    global q
    if request.user.is_authenticated:
        stuff = [cat.category for cat in request.user.following.all()]
    else:
        stuff = []
    if request.method == "POST":
        url = f"https://newsapi.org/v2/everything?q={request.POST.get('q')}"
        if request.POST.get("frmdt"):
            url += f"&from={request.POST.get('frmdt')}"
        if request.POST.get("todt"):
            url += f"&to={request.POST.get('todt')}"
        if request.POST.get("src"):
            url += f"&sources={request.POST.get('src')}"
        if request.POST.get("dom"):
            url += f"&domains={request.POST.get('dom')}"
        url += f"&apiKey={settings.API_KEY}"
        # print(url)

        response = requests.get(url)

        if response.json()["status"] != "ok":
            return render(
                request,
                "news/search.html",
                {
                    "articles": None,
                    "name": request.POST.get("q"),
                    "stuff": stuff,
                    "code": response.json()["code"],
                    "message": response.json()["message"],
                },
            )

        housekeeping(response.json()["articles"], request.POST.get("q"))
        paginator = Paginator(response.json()["articles"], 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "news/search.html",
            {"articles": page_obj, "name": request.POST.get("q"), "stuff": stuff},
        )

    else:
        paginator = Paginator(searcharts, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "news/search.html",
            {"articles": page_obj, "name": q, "stuff": stuff},
        )


# @csrf_exempt
def searchtop(request):
    global searcharts
    global q
    if request.user.is_authenticated:
        stuff = [cat.category for cat in request.user.following.all()]
    else:
        stuff = []
    if request.method == "POST":
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?q={request.POST.get('q-top')}&country={request.POST.get('country')}&category={request.POST.get('category')}&apiKey={settings.API_KEY}"
        )

        if response.json()["status"] != "ok":
            return render(
                request,
                "news/search.html",
                {
                    "articles": None,
                    "name": request.POST.get("q-top"),
                    "stuff": stuff,
                    "code": response.json()["code"],
                    "message": response.json()["message"],
                },
            )

        housekeeping(response.json()["articles"], request.POST.get("q-top"))
        paginator = Paginator(response.json()["articles"], 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "news/search.html",
            {"articles": page_obj, "name": request.POST.get("q-top"), "stuff": stuff},
        )
    else:
        paginator = Paginator(searcharts, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "news/search.html",
            {"articles": page_obj, "name": q, "stuff": stuff},
        )


def category(request, value):
    if request.user.is_authenticated:
        stuff = [cat.category for cat in request.user.following.all()]
    else:
        stuff = []
    response = requests.get(
        f"https://newsapi.org/v2/top-headlines?category={value}&country=in&apiKey={settings.API_KEY}"
    )
    if response.json()["status"] != "ok":
        return render(
            request,
            "news/category.html",
            {
                "articles": None,
                "stuff": stuff,
                "code": response.json()["code"],
                "message": response.json()["message"],
                "name": value.capitalize(),
            },
        )

    paginator = Paginator(response.json()["articles"], 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "news/category.html",
        {"articles": page_obj, "name": value.capitalize(), "stuff": stuff},
    )


# @csrf_exempt
def updateCategory(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        category = Categories.objects.get(category=data.get("category").capitalize())
        if request.user in category.followers.all():
            category.followers.remove(request.user)
            return JsonResponse({"status": False})
        else:
            category.followers.add(request.user)
            return JsonResponse({"status": True})


def feed(request):
    categories = [cat.category for cat in request.user.following.all()]

    if len(categories) == 0:
        return render(
            request,
            "news/feed.html",
            {
                "articles": None,
                "message": "You haven't followed any categories yet,follow them to get curated content from each category in your feed!",
            },
        )

    articles = []
    for category in categories:
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?category={category}&country=in&pageSize=10&apiKey={settings.API_KEY}"
        )
        if response.json()["status"] != "ok":
            continue
        articles.extend(response.json()["articles"])
    paginator = Paginator(articles, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    stuff = [cat.category for cat in request.user.following.all()]

    return render(request, "news/feed.html", {"articles": page_obj, "stuff": stuff})
