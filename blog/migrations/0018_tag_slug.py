# Generated by Django 5.0.4 on 2024-05-01 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
