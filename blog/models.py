from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod


# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="media/%Y/%m", max_length=100, null=True, blank=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']


class Poem(models.Model):
    title = models.CharField(max_length=50,null=True, blank=True)
    content = RichTextUploadingField()
    author = models.CharField(max_length=50,null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    last_updated_time = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']

