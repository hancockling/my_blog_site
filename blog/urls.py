from . import views
from django.urls import path

# namespace
app_name = 'blog'

urlpatterns = [
    path('', views.blog_title, name='blog_title'),
    path('<article_id>', views.blog_acticle, name='blog_detail'),
]
