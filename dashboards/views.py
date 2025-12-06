from urllib import request
from django.shortcuts import render, redirect   
from BlogApp.models import Category
from BlogApp.models import Blogs
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, PostForm, AddUserForm, EditUserForm
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blogs.objects.all().count() 
    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
    }
    return render(request, 'dashboards/dashboard.html', context)

def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'dashboards/categories.html', context)

def add_categories(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    context = {
        'form': form,
    }
    return render(request, 'dashboards/add_categories.html', context)


def edit_categories(request,pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'dashboards/edit_categories.html', context)

def delete_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

def posts(request):
    posts = Blogs.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'dashboards/posts.html', context)

def add_posts(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data.get('title')
            post.slug = slugify(title)
            post.save()
            print("Success")
            return redirect('posts')
        else:
            print("Error!")
            print(form.errors)
    context = {
        'form': form,
    }
    return render(request, 'dashboards/add_posts.html', context)

def edit_posts(request, pk):
    post = get_object_or_404(Blogs, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title)
            post.save()
            return redirect('posts')
    form = PostForm(instance=post)
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'dashboards/edit_posts.html', context)


def delete_posts(request, pk):
    post = get_object_or_404(Blogs, pk=pk)
    post.delete()
    return redirect('posts')


def users(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'dashboards/users.html', context)

def add_users(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = AddUserForm()

    context = {
        'form': form
    }
    return render(request, 'dashboards/add_users.html', context)


def edit_users(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = EditUserForm(instance=user)
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'dashboards/edit_users.html', context)

def delete_users(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')