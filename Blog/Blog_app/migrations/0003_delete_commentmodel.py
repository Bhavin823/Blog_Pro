# Generated by Django 4.2.3 on 2023-08-02 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_app', '0002_commentmodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommentModel',
        ),
    ]
