# Generated by Django 4.1.3 on 2024-03-25 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='cats', to=settings.AUTH_USER_MODEL, verbose_name='Подписчики'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writer', to='news.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='categoryType',
            field=models.CharField(choices=[('NW', 'Новость'), ('AR', 'Статься')], default='AR', max_length=2, verbose_name='Тип поста'),
        ),
        migrations.AlterField(
            model_name='post',
            name='postCategory',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(verbose_name='Содержимое'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_en_us',
            field=models.TextField(null=True, verbose_name='Содержимое'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_ru',
            field=models.TextField(null=True, verbose_name='Содержимое'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_en_us',
            field=models.CharField(max_length=128, null=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_ru',
            field=models.CharField(max_length=128, null=True, verbose_name='Заголовок'),
        ),
    ]