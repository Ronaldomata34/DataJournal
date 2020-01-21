from django.db import models
from django.utils import timezone


class SourceCategory(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name
    
class Source(models.Model):
    slug = models.CharField(max_length=55)
    name = models.CharField(max_length=55)
    description = models.TextField()
    url = models.URLField(max_length=255)
    category = models.ForeignKey('SourceCategory', related_name='article_category', on_delete=models.CASCADE)
    language = models.CharField(max_length=55)
    country = models.CharField(max_length=55)
    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ArticleCategory(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name

class Article(models.Model):
    source = models.ForeignKey('Source', related_name='article_source', on_delete=models.CASCADE)
    category = models.ForeignKey('ArticleCategory', related_name='article_category', on_delete=models.CASCADE)
    author = models.CharField(max_length=55)
    title = models.CharField(max_length=255)
    descripcion = models.TextField()
    url = models.URLField(max_length=255)
    url_image = models.URLField(max_length=255)
    published_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.source.name, self.author)


