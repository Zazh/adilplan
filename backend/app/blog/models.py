import os

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from core.utils.mixins import WebPImageMixin


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

class Post(WebPImageMixin, models.Model):
    objects = models.Manager()
    published = PublishedManager()

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    category = models.CharField(max_length=250, blank=True, verbose_name='Категория поста')
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250, blank=True)
    img = models.ImageField(upload_to='blog/', blank=True, null=True)

    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.make_webp("img")

    def webp_url(self):
        if not self.img or not self.img.name:
            return ""
        url = self.img.url
        return os.path.splitext(url)[0] + ".webp"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ]
        )

class Tags(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=255)