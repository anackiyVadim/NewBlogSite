from django.contrib import admin
from .models import Post, Category, Tegs, Subscribe, PostPhoto, Comment, Profile

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tegs)
admin.site.register(Subscribe)
admin.site.register(PostPhoto)
admin.site.register(Comment)
admin.site.register(Profile)
