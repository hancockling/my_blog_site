# Generated by Django 2.1.5 on 2019-04-16 01:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(blank=True, max_length=100, verbose_name='学校')),
                ('company', models.CharField(blank=True, max_length=100, verbose_name='公司')),
                ('profession', models.CharField(blank=True, max_length=100, verbose_name='职业')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='地址')),
                ('aboutme', models.TextField(blank=True, verbose_name='介绍')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userinfo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Info',
            },
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
