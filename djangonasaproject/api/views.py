from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import UserLoginForm, UserRegisterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def home(request):
    response = requests.get('https://api.nasa.gov/planetary/apod?api_key='+settings.NASA_API_KEY)
    loaded_json = json.loads(response.text)

    daily_image = loaded_json.get('url')
    title = loaded_json.get('title')
    explanation = loaded_json.get('explanation')
    date = loaded_json.get('date')
    owner = loaded_json.get('copyright')

    context = {
        'daily_image': daily_image,
        'title':title,
        'explanation':explanation,
        'date':date,
        'owner':owner
    }

    return render(request, "home.html", context)

@login_required
def search_view(request):
    query = request.GET.get('q')

    if query:
        search_response = requests.get("https://images-api.nasa.gov/search?q="+query+'&media_type=image')
    else:
        search_response = requests.get("https://images-api.nasa.gov/search?q=earth&media_type=image")

    loaded_json = json.loads(search_response.text)
    collection = loaded_json.get('collection')
    items = collection.get('items')

    images=[]
    descriptions=[]
    titles=[]

    for i in items:
        images.append(i.get('links')[0].get('href'))
        descriptions.append(i.get('data')[0].get('description'))
        titles.append(i.get('data')[0].get('title'))

    images=list(zip(images,titles,descriptions))
    paginator = Paginator(images, 4)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    context = {
        'images': images,
    }
    return render(request, "images.html", context) 

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
        'title':'Login'
    }
    return render(request, "login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
        'title':'Register'
    }
    return render(request, "signup.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')

