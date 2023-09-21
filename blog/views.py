from django.shortcuts import render
from .models import Blog, Blog_Comment
from products.models import Main_Category
from cart.models import Wishlist
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def blog_show(request):
    blogs = Blog.objects.all()
    main_categories = Main_Category.objects.all()
    context = {
        'blogs': blogs,
        'main_categories': main_categories,
    }
    return render(request, 'blog/all_blog.html', context)

def blog_details(request, pk):
    main_categories = Main_Category.objects.all()
     
    blog = Blog.objects.get(id=pk)  
    comments = Blog_Comment.objects.filter(blog=blog)
    comment_count = comments.count()
    
    context = {
        'blog': blog,
        'comments': comments,
        'comment_count': comment_count,
        'main_categories': main_categories,
    }
    
    
    return render(request, 'blog/blog_details.html', context)

@login_required
def blog_comments(request, pk):
    get_method =  request.GET.copy()
    comment = get_method.get('comment')
    blog = Blog.objects.get(id=pk)
    user = request.user
    if comment is not None and blog is not None:
        Blog_Comment.objects.create(user=user, blog=blog, comment_text=comment)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))