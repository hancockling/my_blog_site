from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import ArticlePost, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .forms import CommentForm
from django.db.models import Count
"""这里编写的都是前台展示的视图"""


def article_titles(request, username=None):
    """文章列表"""
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        articles_title = ArticlePost.objects.all()

    paginator = Paginator(articles_title, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)     # 获取指定页面内容，其参数必须>=1的整数
        articles = current_page.object_list  # 获取当前页对应的所有记录
    except PageNotAnInteger:        # 页码不是整数，捕获异常
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:       # 页码为空，捕获异常
        current_page = paginator.page(paginator.num_pages)      # 返回页数
        articles = current_page.object_list

    if username:
        return render(request, 'article/list/author_titles.html', {'articles': articles, 'page': current_page,
                                                                    'userinfo': userinfo, 'user': user})
    return render(request, 'article/list/article_titles.html', {'articles': articles, 'page': current_page})


def article_detail(request, id, slug):
    """文章详情"""
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # values_list的作用就是得到article对象的属性article_tag的id列表，即得到当前文章的所有标签在数据库表中的id值
    # 声明flat=True，返回的类型是列表；如果不声明，列表是由元组组成
    article_tags_ids = article.article_tag.values_list('id', flat=True)
    # 找出具有相同标签id的所有文章，并用exclude排除当前文章
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('article_tag')).order_by('-same_tags', '-created')[:4]
    return render(request, 'article/list/article_detail.html', {'article': article, 'comments': comments,
                                                                'similar_articles': similar_articles})


@login_required
@csrf_exempt
@require_POST
def like_article(request):
    """点赞"""
    article_id = request.POST['id']     # 另外一种写法：request.POST.get("id")
    action = request.POST['action']
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                if request.user in article.users_like.all():
                    # 判断请求的用户是否在点赞的QuerySet里面，判断是否已经点过赞
                    return HttpResponse("0")
                else:
                    article.users_like.add(request.user)
                    return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")


@login_required
@require_POST
def post_comment(request, article_id):
    """文章评论"""
    article = get_object_or_404(ArticlePost, id=article_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article = article
        new_comment.commentator = request.user
        new_comment.save()
        return redirect('article:list_article_detail', article.id, article.slug)
    else:
        return HttpResponse("表单内容有误，请重新填写。")

