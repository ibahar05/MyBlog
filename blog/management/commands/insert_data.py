from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone

from accounts.models import User, Profile
from blog.models import Post, Category

Category_list = [
    "IT",
    "Food",
    "Animal",
    "Home",
    "Design",
    "Music",
    "Art",
    "Sport",
    "Car",
    "Love",
    "nature",
    "Shop",
    "Fashion",
]


class Command(BaseCommand):
    help = "Inseting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **actions):
        user = User.objects.create_user(email=self.fake.email(), password="134679@xxB")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.save()

        for name in Category_list:
            Category.objects.get_or_create(name=name)

        for _ in range(20):
            Post.objects.create(
                author=profile,
                title=self.fake.paragraph(nb_sentences=1),
                content=self.fake.paragraph(nb_sentences=5),
                status=random.choice([True, False]),
                category=Category.objects.get(name=random.choice(Category_list)),
                published_date=timezone.now(),
            )
