from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import ArticleColumn, ArticlePost, ArticleTag
from .forms import ArticleColumnForm, ArticlePostForm, ArticleTagForm
import json
# Create your views here.
"""这里编写的都是用户后台的视图：栏目管理/发布文章/文章管理"""


@login_required
@csrf_exempt
def article_column(request):
    """栏目列表 & 新增栏目"""
    if request.method == "GET":
        column_list = ArticleColumn.objects.filter(user=request.user)
        paginator = Paginator(column_list, 10)  # 实例化一个分页对象, 每页显示10个
        page = request.GET.get('page')  # 从URL通过get页码，如?page=3
        try:
            current_page = paginator.page(page)  # 获取指定页面内容，其参数必须>=1的整数
            columns = current_page.object_list  # 获取当前页对应的所有记录
        except PageNotAnInteger:  # 页码不是整数，捕获异常
            current_page = paginator.page(1)
            columns = current_page.object_list
        except EmptyPage:  # 页码为空，捕获异常
            current_page = paginator.page(paginator.num_pages)  # 返回页数
            columns = current_page.object_list
        column_form = ArticleColumnForm()
        return render(request, 'article/column/article_column.html', {"columns": columns, "column_form": column_form,
                                                                      "page": current_page})
    if request.method == "POST":
        column_name = request.POST['column']
        if column_name:
            columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
            if columns:
                return HttpResponse('2')
            else:
                ArticleColumn.objects.create(user=request.user, column=column_name)
                return HttpResponse('1')
        else:
            return HttpResponse('3')


@login_required
@require_POST
@csrf_exempt
def rename_article_column(request):
    """修改栏目"""
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required
@require_POST
@csrf_exempt
def del_article_column(request):
    """删除栏目"""
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required
@csrf_exempt
def article_post(request):
    """新增文章"""
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        return render(request, 'article/column/article_post.html',
                      {'article_post_form': article_post_form, 'article_columns': article_columns,
                       'article_tags': article_tags})


@login_required
def article_list(request):
    """文章列表"""
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 10)  # 实例化一个分页对象, 每页显示10个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    try:
        current_page = paginator.page(page)     # 获取指定页面内容，其参数必须>=1的整数
        articles = current_page.object_list  # 获取当前页对应的所有记录
    except PageNotAnInteger:        # 页码不是整数，捕获异常
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:       # 页码为空，捕获异常
        current_page = paginator.page(paginator.num_pages)      # 返回页数
        articles = current_page.object_list
    return render(request, 'article/column/article_list.html', {'articles': articles, 'page': current_page})


@login_required
def article_detail(request, id, slug):
    """文章详情"""
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, 'article/column/article_detail.html', {'article': article})


@login_required
@require_POST
@csrf_exempt
def del_article(request):
    """删除文章"""
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required
@csrf_exempt
def redit_article(request, article_id):
    """修改文章"""
    if request.method == "GET":
        article_columns = request.user.article_column.all()     # 该用户的所有栏目
        article = ArticlePost.objects.get(id=article_id)        # 当前ID的这篇文章的实例
        this_article_form = ArticlePostForm(initial={"title": article.title})  # 当前ID的这篇文章实例的表单，初始标题
        this_article_column = article.column        # 当前ID的这篇文章实例的默认栏目
        user_tags = request.user.tag.all()       # 该用户的所有标签，注意：不是这篇文章的所有标签
        return render(request, 'article/column/redit_article.html', {"article": article,
                                                                     "article_columns": article_columns,
                                                                     "this_article_column": this_article_column,
                                                                     "this_article_form": this_article_form,
                                                                     'user_tags': user_tags})
    else:
        edited_article = ArticlePost.objects.get(id=article_id)
        edited_article.article_tag.clear()      # 先清空此文章的所有标签，如果不清空，就永远是累加
        try:
            edited_article.column = request.user.article_column.get(id=request.POST['column_id'])
            edited_article.title = request.POST['title']
            edited_article.body = request.POST['body']
            edited_article.save()
            tags = request.POST['tags']
            if tags:
                for atag in json.loads(tags):
                    tag = request.user.tag.get(tag=atag)
                    edited_article.article_tag.add(tag)
            return HttpResponse("1")
        except:
            return HttpResponse("2")


@login_required
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request, 'article/tag/tag_list.html', {'article_tags': article_tags,
                                                             'article_tag_form': article_tag_form})
    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("数据没有被保存")
        else:
            return HttpResponse("对不起，表单不合法")


@login_required
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")
