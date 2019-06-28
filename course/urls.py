from django.urls import path
from django.views.generic import TemplateView
from . import views
# namespace
app_name = 'course'

urlpatterns = [
    path('about/', TemplateView.as_view(template_name='course/about.html'), name='about'),
    path('course-list/', views.CourseListView.as_view(), name='course_list'),
    path('manage-course/', views.ManageCourseListView.as_view(), name='manage_course'),
    path('create-course/', views.CreateCourseView.as_view(), name='create_course'),
    path('delete-course/<pk>', views.DeleteCourseView.as_view(), name='delete_course'),
    path('create-lesson/', views.CreateLessonView.as_view(), name='create_lesson'),
]
