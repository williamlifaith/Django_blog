from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def blog_list(request):
    # context = {}
    # context['blogs'] = Blog.objects.all()
    context = {}
    blogs_list = Blog.objects.all()
    # 分页器，对 beatles_list 进行分页操作，每页显示2个对象
    paginator = Paginator(blogs_list, 5)
    # get 方法获取页数
    page = request.GET.get('page')

    try:  # 获取某页
        blogs_list = paginator.page(page)
    except PageNotAnInteger:  # 如果 page 参数不为正整数，显示第一页
        blogs_list = paginator.page(1)
    except EmptyPage:  # 如果 page 参数为空页，跳到最后一页
        blogs_list = paginator.page(paginator.num_pages)

    context['blogs_list'] = blogs_list
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")
    return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")

    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_list = Blog.objects.filter(blog_type=blog_type)
    # 分页器，对 beatles_list 进行分页操作，每页显示2个对象
    paginator = Paginator(blogs_list, 5)
    # get 方法获取页数
    page = request.GET.get('page')

    try:  # 获取某页
        blogs_list = paginator.page(page)
    except PageNotAnInteger:  # 如果 page 参数不为正整数，显示第一页
        blogs_list = paginator.page(1)
    except EmptyPage:  # 如果 page 参数为空页，跳到最后一页
        blogs_list = paginator.page(paginator.num_pages)
    context['blogs_list'] = blogs_list
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    context = {}
    blogs_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    # 分页器，对 beatles_list 进行分页操作，每页显示2个对象
    paginator = Paginator(blogs_list, 5)
    # get 方法获取页数
    page = request.GET.get('page')

    try:  # 获取某页
        blogs_list = paginator.page(page)
    except PageNotAnInteger:  # 如果 page 参数不为正整数，显示第一页
        blogs_list = paginator.page(1)
    except EmptyPage:  # 如果 page 参数为空页，跳到最后一页
        blogs_list = paginator.page(paginator.num_pages)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    context['blogs_list'] = blogs_list
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")
    return render_to_response('blog/blogs_with_date.html', context)
