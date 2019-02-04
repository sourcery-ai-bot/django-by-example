from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    Manager,
    Model,
    SlugField,
    TextField,
)


class PublishedManager(Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(Model):
    STATUS_CHOICES = (("draft", "Draft"), ("published", "Published"))

    title = CharField(max_length=250)
    slug = SlugField(max_length=250, unique_for_date="publish")
    author = ForeignKey(User, on_delete=CASCADE, related_name="blog_posts")
    body = TextField()
    publish = DateTimeField(default=timezone.now)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    status = CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    # Model Managers
    objects = Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class Comment(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name="comments")
    name = CharField(max_length=80)
    email = EmailField()
    body = TextField()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    active = BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
