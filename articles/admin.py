from django.contrib import admin

from .models import Article, Source

class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'url', 'to_scrape']
    list_filter = ('category',) 
    list_editable = ('to_scrape',)
    search_fields = ('name',)
    #exclude = ('year_from_code', 'year_to_code')

admin.site.register(Article)
admin.site.register(Source, SourceAdmin)


# Register your models here.
