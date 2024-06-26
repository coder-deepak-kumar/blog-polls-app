# Generated by Django 5.0.4 on 2024-05-01 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='feature_img',
            field=models.ImageField(blank=True, null=True, upload_to='image/feature_img/'),
        ),
        migrations.AddField(
            model_name='post',
            name='thumbnail_img',
            field=models.ImageField(blank=True, null=True, upload_to='image/thumbnail_img/'),
        ),
    ]
