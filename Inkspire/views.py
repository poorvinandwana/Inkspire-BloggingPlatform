from django.shortcuts  import render,redirect
from BlogApp.models import Category,Blogs
from .forms import RegistraionForm
# from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    categories = Category.objects.all()
    featured_post = Blogs.objects.filter(is_featured=True,status='published')
    posts = Blogs.objects.filter(is_featured=False, status='published').order_by('-created_at')
    print(featured_post)
    
    context = {
        'categories':categories,
        'featured_post':featured_post,
        'posts':posts
    }
    return render(request, 'home.html', context)




def register(request):
    if request.method == "POST":
        form = RegistraionForm(request.POST)
        if form.is_valid():
            user = form.save()        
            auth_login(request, user)       
            return redirect('home')  
    else:
        form = RegistraionForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context)




def login_view(request):
    if request.method=="POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('home')
    else:
        form  = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'login.html',context)


def logout(request):
    auth.logout(request)
    return redirect('home')