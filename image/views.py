from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from .models import Image
# Create your views here.


@login_required
@csrf_exempt
def upload_image(request):
    """添加网络图片"""
    if request.method == "POST":
        form = ImageForm(data=request.POST)
        if form.is_valid():
            try:
                new_item = form.save(commit=False)
                new_item.user = request.user
                new_item.save()
                return JsonResponse({'status': '1'})
            except:
                return JsonResponse({'status': '0'})
        else:
            return JsonResponse({'status': '2'})
    else:
        return render(request, 'image/upload_image.html',)


@login_required
def list_images(request):
    """网络图片列表"""
    images = Image.objects.filter(user=request.user)
    return render(request, 'image/list_images.html', {'images': images})


@login_required
@csrf_exempt
@require_POST
def del_image(request):
    """删除网络图片"""
    image_id = request.POST['image_id']
    try:
        image = Image.objects.get(id=image_id)
        image.delete()
        return JsonResponse({'status': "1"})
    except:
        return JsonResponse({'status': "2"})


def falls_images(request):
    images = Image.objects.all()
    return render(request, 'image/falls_images.html', {"images": images})
