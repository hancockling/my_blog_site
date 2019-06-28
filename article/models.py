from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify
# Create your models here.


class ArticleColumn(models.Model):
    user = models.ForeignKey(User, related_name='article_column',
                             on_delete=models.CASCADE, verbose_name='作者')
    column = models.CharField('栏目', max_length=200)
    created = models.DateField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.column


class ArticleTag(models.Model):
    author = models.ForeignKey(User, related_name='tag', on_delete=models.CASCADE, verbose_name='作者')
    tag = models.CharField('标签', max_length=500)

    def __str__(self):
        return self.tag


class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name='article',
                               on_delete=models.CASCADE, verbose_name='作者')
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('Slug', max_length=500)
    column = models.ForeignKey(ArticleColumn, related_name='article_column',
                               on_delete=models.CASCADE, verbose_name='栏目')
    body = models.TextField()
    created = models.DateTimeField('创建时间', default=timezone.now)
    updated = models.DateTimeField('修改时间', auto_now=True)
    users_like = models.ManyToManyField(User, related_name='articles_like', blank=True, verbose_name='点赞')
    total_views = models.PositiveIntegerField('浏览量', default=0)
    article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True, verbose_name='文章标签')

    class Meta:
        ordering = ['-updated']
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id, self.slug])

    def get_url_path(self):
        return reverse('article:list_article_detail', args=[self.id, self.slug])


class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, related_name='comments', on_delete=models.CASCADE, verbose_name='文章')
    commentator = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, verbose_name='评论人')
    body = models.TextField()
    created = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username, self.article)
