from django.db import models
from django.urls import reverse

from autoslug.fields import AutoSlugField

from accounts.models import Profile

# Create your models here.
class Post(models.Model):
    owner_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Post title', max_length=500)
    content = models.CharField(verbose_name='Post content', max_length=20000)
    # slug_title = models.SlugField(verbose_name='Post slug', max_length=200, unique=True)
    slug_title = AutoSlugField(populate_from='title', verbose_name='Post slug', max_length=200, unique=True)
    tag = models.CharField(verbose_name='Post tag', max_length=20, choices=Profile.plan_options, default='fr')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ['-date_updated']

    def __str__(self):
        return f"{self.title} by {self.owner_profile.user.username}"
    
    def get_absolute_url(self):
        return reverse('blog:view-post', kwargs={'post_slug': self.slug_title})