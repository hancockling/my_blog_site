from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    birth = models.DateField('生日', blank=True, null=True)
    phone = models.CharField('电话', max_length=20, blank=True, null=True)
    mod_date = models.DateTimeField('最后修改时间', auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profile'

    def __str__(self):
        return 'user {}'.format(self.user.username)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userinfo')
    school = models.CharField('学校', max_length=100, blank=True)
    company = models.CharField('公司', max_length=100, blank=True)
    profession = models.CharField('职业', max_length=100, blank=True)
    address = models.CharField('地址', max_length=100, blank=True)
    aboutme = models.TextField('介绍', blank=True)
    photo = models.ImageField(blank=True)

    class Meta:
        verbose_name = 'User Info'
        verbose_name_plural = 'User Info'

    def __str__(self):
        return 'user {}'.format(self.user.username)
