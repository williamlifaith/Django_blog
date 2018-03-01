from django.contrib import admin
from .models import BlogType, Blog
from .models import Poem


# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'get_read_num', 'author', 'created_time', 'last_updated_time')


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'author', 'created_time', 'last_updated_time')
