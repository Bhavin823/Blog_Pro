from django.core.management.base import BaseCommand
from Blog_app.models import PostModel, create_slug  # Import your models and slug creation function

class Command(BaseCommand):
    help = 'Populate slugs for posts without slugs'

    def handle(self, *args, **kwargs):
        posts_without_slugs = PostModel.objects.filter(slug__isnull=True)
        for post in posts_without_slugs:
            post.slug = create_slug(post)
            post.save()
            self.stdout.write(self.style.SUCCESS(f'Slug populated for post: {post.title}'))
