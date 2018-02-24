from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='博客标题')
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING, verbose_name='分类')
    content = models.TextField(verbose_name='博客内容')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    last_updated_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="media/%Y/%m", max_length=100,null=True,blank=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']
