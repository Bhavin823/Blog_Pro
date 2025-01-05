# Generated by Django 4.2.3 on 2024-12-30 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Blog_app', '0015_postmodel_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
