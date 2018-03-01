from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read


# Create your views here.
def get_blog_list_common_data(request, blogs_list):
    # 分页器，对 beatles_list 进行分页操作，每页显示5个对象
    paginator = Paginator(blogs_list, 5)
    # get 方法获取页数
    page = request.GET.get('page')

    try:  # 获取某页
        blogs_list = paginator.page(page)
    except PageNotAnInteger:  # 如果 page 参数不为正整数，显示第一页
        blogs_list = paginator.page(1)
    except EmptyPage:  # 如果 page 参数为空页，跳到最后一页
        blogs_list = paginator.page(paginator.num_pages)

    # 获取博客分类的对应博客数量
    # 第二种方法：BlogType.objects.annotate(Count('blog'))
    '''第一种方法blog_types = BlogType.object.all()
        blog_types_list = []
        for blog_type in blog_types:
            blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
            blog_types_list.append(blog_type)'''

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs_list'] = blogs_list
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blogs_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_list)
    return render_to_response('blog/blog_list.html', context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_list)

    return render_to_response('blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blogs_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render_to_response('blog/blogs_with_date.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")

    response = render_to_response('blog/blog_detail.html', context)  # 响应
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记

    return render_to_response('blog/blog_detail.html', context)
