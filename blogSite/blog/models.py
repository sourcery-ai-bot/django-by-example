from django.utils import timezone
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
#    SlugField,
    TextField,
)

class PublishedManager(Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    # Mode Fields
    title = CharField(
        max_length=250
    )
    slug = AutoSlugField(
        max_length=250,
        populate_from='title',
        unique_for_date='publish',
    )
    author = ForeignKey(
        User,
        related_name='blog_posts',
        on_delete=CASCADE
    )
    body = TextField()
    publish = DateTimeField(
        default=timezone.now
    )
    created = DateTimeField(
        auto_now_add=True
    )
    updated = DateTimeField(
        auto_now=True
    )
    status = CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    # Model Managers
    objects = Manager()
    published = PublishedManager()

    class Meta:
        ordering = [
            '-publish',
        ]

    def __str__(self):
        return self.title

