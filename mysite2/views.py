import datetime
from django.shortcuts import render_to_response
from blog.models import Poem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Sum
from blog.models import Blog


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date).values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:7]


def home_page(request):
    poem_list = Poem.objects.all()
    paginator = Paginator(poem_list, 1)
    # get 方法获取页数
    page = request.GET.get('page')

    try:  # 获取某页
        poem_list = paginator.page(page)
    except PageNotAnInteger:  # 如果 page 参数不为正整数，显示第一页
        poem_list = paginator.page(1)
    except EmptyPage:  # 如果 page 参数为空页，跳到最后一页
        poem_list = paginator.page(paginator.num_pages)

    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days',hot_blogs_for_7_days,3600)

    context = {}
    context['dates'] = dates
    context['poem_list'] = poem_list
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    return render_to_response('home.html', context)
