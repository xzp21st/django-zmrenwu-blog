import markdown

from slugify import slugify
from django.shortcuts import render, get_object_or_404, redirect
from markdown.extensions.toc import TocExtension

from .models import Post, Category


def header_slugify(value, separator='-'):
    return slugify(value, separator=separator)


"""
使用下方的模板引擎方式。
def index(request):
    return HttpResponse("欢迎访问我的博客首页！")
"""

"""
使用下方真正的首页视图函数
def index(request):
    return render(request, 'blog/index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页'
    })
"""


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=header_slugify)
    ])
    post.body = md.convert(post.body)
    try:
        previous_post = post.get_previous_by_created_time()
    except Post.DoesNotExist:
        previous_post = None

    try:
        next_post = post.get_next_by_created_time()
    except Post.DoesNotExist:
        next_post = None

    return render(request, 'blog/detail.html', context={'post': post,
                                                        'toc': md.toc,
                                                        'previous_post': previous_post,
                                                        'next_post': next_post})


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    return redirect(cate, permanent=True)


def category_slug(request, slug):
    cate = get_object_or_404(Category, slug=slug)
    post_list = Post.objects.filter(category=cate)

    if cate.get_genre_display() == 'tutorial':
        post_list = post_list.order_by('created_time')
        return render(request, 'blog/tutorial.html', context={'post_list': post_list,
                                                              'category': cate})
    return render(request, 'blog/category.html', context={'post_list': post_list,
                                                          'category': cate})
