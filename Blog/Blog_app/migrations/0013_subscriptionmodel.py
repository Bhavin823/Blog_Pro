# Generated by Django 4.2.3 on 2024-12-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_app', '0012_contactmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='subscriptionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
