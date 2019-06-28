from django import template
from article.models import ArticlePost
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
register = template.Library()


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()


@register.simple_tag
def author_total_articles(user):
    return user.article.count()


@register.simple_tag
def show_total_views(n=5):
    return ArticlePost.objects.all().order_by('-total_views')[:n]


@register.inclusion_tag('article/list/latest_articles.html')
def show_latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by('-created')[:n]
    return {'latest_articles': latest_articles}


@register.simple_tag
def most_commented_articles(n=5):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:n]


@register.filter(name='markdown')       # 重命名自定义模板过滤器的名字，即把markdown_filter修改为markdown
def markdown_filter(text):              # 避免使用markdown作为函数名，否则与第三方库的名字冲突
    return mark_safe(markdown.markdown(text))
