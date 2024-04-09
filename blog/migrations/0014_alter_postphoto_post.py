# Generated by Django 4.1 on 2024-04-01 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_postphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postphoto',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.post', verbose_name='Пост'),
        ),
    ]
