from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from blog.models import Category, Blog
import random
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate blog with sample categories and posts for development.'

    def handle(self, *args, **options):
        User = get_user_model()
        # Get or create a bot user
        user, created = User.objects.get_or_create(username='blogbot', defaults={
            'email': 'blogbot@example.com',
            'is_staff': True,
        })
        if created:
            user.set_password('blogbotpass')
            user.save()

        categories = ['Announcements', 'Tutorials', 'Events', 'Competitions', 'Projects']
        cat_objs = []
        for name in categories:
            c, _ = Category.objects.get_or_create(name=name)
            cat_objs.append(c)

        sample_contents = [
            '<p>This is a sample post for the ICE Programming Club. Welcome to our blog!</p>',
            '<p>Learn about algorithms, data structures, and contest strategies.</p>',
            '<p>Event recap: Our recent hackathon had amazing projects. Highlights below.</p>',
            '<p>Tutorial: Getting started with Django and building production-ready apps.</p>',
            '<p>Competition prep guide: How to train effectively for ICPC-style contests.</p>',
        ]

        created_posts = 0
        now = timezone.now()
        for i in range(1, 11):
            title = f"Sample Post #{i} - {random.choice(['Intro','Guide','Recap','Tips','Deep Dive'])}"
            short = 'This is a short summary of the sample post. Read to learn more.'
            content = random.choice(sample_contents) * 3
            category = random.choice(cat_objs)
            created_at = now - timedelta(days=random.randint(0, 60))
            post, created = Blog.objects.get_or_create(
                title=title,
                defaults={
                    'author': user,
                    'short_description': short,
                    'content': content,
                    'category': category,
                    'is_published': True,
                    'created_at': created_at,
                }
            )
            if created:
                created_posts += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_posts} sample posts and {len(cat_objs)} categories.'))
