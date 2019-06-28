from django.contrib import admin
from .models import UserProfile, UserInfo
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth', 'phone', 'mod_date']
    list_filter = ['phone']


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'school', 'company', 'profession', 'address', 'aboutme']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
