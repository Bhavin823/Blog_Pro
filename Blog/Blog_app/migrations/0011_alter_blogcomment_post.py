# Generated by Django 4.2.3 on 2024-12-02 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_app', '0010_blogcomment_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Blog_app.postmodel'),
        ),
    ]
