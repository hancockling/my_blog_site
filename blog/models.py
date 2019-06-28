from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class BlogArticles(models.Model):
    title = models.CharField('标题', max_length=300)
    author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE, verbose_name='作者')
    body = models.TextField('内容')
    publish = models.DateTimeField('发布时间', default=timezone.now)

    class Meta:
        ordering = ['-publish']
        verbose_name = 'Blog Articles'
        verbose_name_plural = 'Blog Articles'

    def __str__(self):
        return self.title
