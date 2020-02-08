from django.contrib import admin

from .models import Publisher, Article

admin.site.register(Publisher)
admin.site.register(Article)