from . import views
from django.urls import path
from django.contrib.auth.views import LoginView
# namespace
app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='user_login'),
    path('logout/', views.logout_view, name='user_logout'),
    path('register/', views.register, name='register'),
    path('my-information/', views.myself, name='my_information'),
    path('edit-my-information/', views.myself_edit, name='edit_my_information'),
    path('my-image/', views.my_image, name='my_image'),
]
