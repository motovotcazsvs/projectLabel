# Generated by Django 3.0.6 on 2021-06-20 15:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appSocialNetwork', '0003_auto_20200829_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description_book',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание книги'),
        ),
        migrations.RemoveField(
            model_name='book',
            name='like_author',
        ),
        migrations.AddField(
            model_name='book',
            name='like_author',
            field=models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='like_publication',
            field=models.IntegerField(default=0, verbose_name='Likes'),
        ),
    ]
