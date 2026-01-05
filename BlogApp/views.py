from django.shortcuts import render, redirect, get_object_or_404
from . models import Blogs, Category, Comments
from django.db.models import Q

def posts_by_category(request, category_id):
    posts = Blogs.objects.filter(status='published', category_id=category_id)

    
    category = get_object_or_404(Category, pk=category_id)


    context = {
        'posts':posts,
        'category' : category
    }
    return render(request, 'posts_by_category.html', context)

def blogs(request, slug):
    single_post = get_object_or_404(Blogs, slug=slug, status='published')
    if request.method == 'POST':
        comment = Comments()
        comment.user = request.user
        comment.blog = single_post
        comment.comment = request.POST.get('comment')
        comment.save()
        return redirect('blogs', slug=slug)

    comments = Comments.objects.filter(blog=single_post)
    comment_count = comments.count()
    print("Comments: ", comments)
    context = {
        'single_post':single_post,
        'comments': comments,
        'comment_count': comment_count                   
    }
    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    # print(keyword)
    blogs = Blogs.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='published')
    print("Value: ", blogs)
    content={
        'blogs': blogs,
        'keyword': keyword
    }
    return render(request, 'search.html', content)
