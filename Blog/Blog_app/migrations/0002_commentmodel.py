# Generated by Django 4.2.3 on 2023-08-02 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('comment_text', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Blog_app.commentmodel')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Blog_app.postmodel')),
            ],
        ),
    ]
