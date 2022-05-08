# Generated by Django 3.2.13 on 2022-05-07 17:33

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import readStatistics.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='类名')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('alter_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('avatar', imagekit.models.fields.ProcessedImageField(upload_to='article/%Y%m%d')),
            ],
            options={
                'verbose_name': '文章类型',
                'db_table': 'db_blog_articlecategory',
                'ordering': ['-alter_time'],
            },
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=80, verbose_name='作者')),
                ('title', models.CharField(max_length=80, verbose_name='标题')),
                ('content', ckeditor.fields.RichTextField()),
                ('abstract', models.TextField(blank=True, max_length=50, null=True, verbose_name='摘要')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('alter_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('status', models.CharField(choices=[('d', 'Draft'), ('p', 'Publish')], max_length=1, verbose_name='文章状态')),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('like_number', models.PositiveIntegerField(default=0, verbose_name='点赞数')),
                ('page_view', models.PositiveIntegerField(default=0, verbose_name='阅读量')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.articlecategory', verbose_name='文章类型')),
                ('tag', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': '文章数据表',
                'db_table': 'db_blog_article',
                'ordering': ['-alter_time'],
            },
            bases=(models.Model, readStatistics.models.ReadNumExpandMethod),
        ),
    ]
