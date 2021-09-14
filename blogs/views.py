from urllib.parse import urlparse
from accounts.models import Business
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import BlogActivation, Category, Blog, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .models import Blog,Category
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q


def blog(request, slug=None):
    # Check if the blog is activated or not
    business = Business.objects.get(user__is_business=True, is_account_verified=True)
    blog_activation = BlogActivation.objects.get(business=business)
    if not blog_activation.is_enabled:
        return redirect('home')
    

    categories = None
    blogs =None
    paged_blogs=None
    blog_count =0
    category = Category.objects.all()

    blogs = Blog.objects.all().filter(status = 1).order_by('-id')
    recent_blogs = blogs.filter(status = 1).order_by('-id')[:2]
    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    paged_blogs = paginator.get_page(page)
    blog_count = blogs.count()



    if slug != None:
        categories = get_object_or_404(Category, slug=slug).get_descendants(include_self=True)
        recent_blogs = blogs.filter(status = 1).order_by('-id')[:2]
        cblogs = Blog.objects.filter(category__in=categories)
        paginator = Paginator(cblogs, 10)
        page = request.GET.get('page')
        paged_blogs = paginator.get_page(page)
        blog_count = cblogs.count()


    if 'keyword' in request.GET: #?keyword=politics
        keyword = request.GET['keyword']
        if keyword:
            blogs = blogs.filter(Q(title__icontains=keyword) | Q(blog_body__icontains=keyword) | Q(short_description__icontains=keyword))
            recent_blogs = blogs.filter(status = 1).order_by('-id')[:2]
            paginator = Paginator(blogs, 10)
            page = request.GET.get('page')
            paged_blogs = paginator.get_page(page)
            blog_count = blogs.count()


    context = {
    'blogs': paged_blogs,
    'blog_count': blog_count,
    'category': category,
    'values' : request.GET,
    'recent_blogs' : recent_blogs,
    }

    return render(request, 'blogs/blogs.html', context)


def blog_detail(request, category_slug, blog_slug):
    # Check if the blog is activated or not
    business = Business.objects.get(user__is_business=True, is_account_verified=True)
    blog_activation = BlogActivation.objects.get(business=business)
    if not blog_activation.is_enabled:
        return redirect('home')
        
    try:
        single_blog = Blog.objects.get(category__slug=category_slug, slug=blog_slug)
        # If the blog is set to draft, it will be unavailable for public
        if single_blog.status == 0:
            if request.user.is_authenticated:
                if request.user.is_business == True:
                    pass
                else:
                    # If the authenticated user is not the business user, redirect him to all blogs
                    return redirect('blog')
            else:
                # If the user is not at all autheticated, redirect him to all blogs
                return redirect('blog')
        comments = single_blog.comments.filter(is_active=True, reply=None)
        new_comment = None
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            comments_count = comments.count()
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.blog_id = single_blog.id
                reply_id = request.POST.get('reply_id')
                comment_body = request.POST.get('comment_body')
                reply_qs =None
                if reply_id:
                    reply_qs = Comment.objects.get(id=reply_id)
                new_comment = Comment.objects.create(
                    user = request.user,
                    blog = single_blog,
                    comment_body = comment_body,
                    reply=reply_qs
                )
                new_comment.save()
                response_data = {}
                response_data['status'] = 'success'
                return JsonResponse(response_data, content_type="application/json")

        else:
            comment_form = CommentForm()
            comments_count = comments.count()

    except Exception as e:
        raise e
    context = {
        'single_blog': single_blog,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'comments_count':comments_count,
        # 'replies': replies,
        }
    return render(request, 'blogs/blog_detail.html', context)
