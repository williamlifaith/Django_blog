from django.shortcuts import render_to_response
from blog.models import Poem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from read_statistics.utils import get_seven_days_read_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog


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
    read_nums = get_seven_days_read_data(blog_content_type)
    context = {}
    context['poem_list'] = poem_list
    context['read_nums'] = read_nums
    return render_to_response('home.html', context)

