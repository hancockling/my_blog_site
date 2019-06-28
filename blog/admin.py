from django.contrib import admin
from .models import BlogArticles
# Register your models here.


class BlogActiclesAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish']
    list_filter = ['publish', 'author']
    search_fields = ['title', 'body']
    # 外键不再是下拉框选项，而是填写ID，可以点搜索按钮查询外键ID，这个属性非常有用
    raw_id_fields = ['author', ]
    date_hierarchy = 'publish'
    ordering = ['publish', 'author']


admin.site.register(BlogArticles, BlogActiclesAdmin)

