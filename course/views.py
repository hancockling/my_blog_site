from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Course, Lesson
from .forms import CreateCourseForm, CreateLessonForm
from django.http import HttpResponse
import json
# Create your views here.


# 创建 UserMixin类，表示这个类将用于后面的类中，而不是作为视图使用
class UserMixin:
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model = Course


class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = 'courses'
    template_name = 'course/manage/manage_course_list.html'


class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'course/course_list.html'


class CreateCourseView(UserCourseMixin, CreateView):
    fields = ['title', 'overview']
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kwargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect('course:manage_course')
        return self.render_to_response({'form': form})


class DeleteCourseView(UserCourseMixin, DeleteView):
    # template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy('course:manage_course')

    def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp


class CreateLessonView(LoginRequiredMixin, CreateView):
    model = Lesson
    template_name = 'course/manage/create_lesson.html'

    # def get(self, request, *args, **kwargs):
    #     form = CreateLessonForm(user=self.request.user)
    #     return render(request, 'course/manage/create_lesson.html', {'form': form})
    #
    # def post(self, request, *args, **kwargs):
    #     form = CreateLessonForm(self.request.user, request.POST, request.FILES)
    #     if form.is_valid():
    #         new_lesson = form.save(commit=False)
    #         new_lesson.user = self.request.user
    #         new_lesson.save()
    #         return redirect("course:manage_course")
