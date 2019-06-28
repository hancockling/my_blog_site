from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserInfo
from django.contrib.auth.models import User
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def logout_view(request):
    """注销用户"""
    logout(request)
    return HttpResponseRedirect(reverse('account:user_login'))


def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            UserInfo.objects.create(user=new_user)
            UserProfile.objects.create(user=new_user)
            # 让用户自动登录，再重定向到主页
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('home'))
    context = {'form': form}
    return render(request, 'account/register.html', context)


@login_required
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, 'account/myself.html', {'user': user, 'userprofile': userprofile, 'userinfo': userinfo})


@login_required
def myself_edit(request):
    """修改个人信息"""
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    user_info = get_object_or_404(UserInfo, user=user)

    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            user_profile.birth = form.cleaned_data['birth']
            user_profile.phone = form.cleaned_data['phone']
            user_profile.save()

            user_info.school = form.cleaned_data['school']
            user_info.company = form.cleaned_data['company']
            user_info.profession = form.cleaned_data['profession']
            user_info.address = form.cleaned_data['address']
            user_info.aboutme = form.cleaned_data['aboutme']
            user_info.save()

            return HttpResponseRedirect(reverse('account:my_information'))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                        'birth': user_profile.birth, 'phone': user_profile.phone,
                        'school': user_info.school, 'company': user_info.company, 'profession': user_info.profession,
                        'address': user_info.address, 'aboutme': user_info.aboutme}
        form = UserForm(default_data)

    return render(request, 'account/myself_edit.html', {'form': form, 'user': user, 'userinfo': user_info})


@login_required
@csrf_exempt
def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        user_info = UserInfo.objects.get(user=request.user.id)
        user_info.photo = img
        user_info.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html',)
