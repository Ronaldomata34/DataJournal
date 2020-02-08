from django.db import models
from django.utils import timezone

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=55)
    url = models.URLField(max_length=255)
    country = models.CharField(max_length=55)
    to_scrape = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    publisher = models.ForeignKey('Publisher', related_name='article_publisher', on_delete=models.CASCADE)
    url = models.URLField(max_length=255)
    section = models.CharField(max_length=55)
    subsection = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    author = models.CharField(max_length=55)
    headline = models.CharField(max_length=255)
    content = models.TextField()
    content_length = models.IntegerField()
    published_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.publisher.name, self.author)


"""Publisher (meta og:site_name) - e.g. Mirror
Article URL - e.g. https://www.mirror.co.uk/sport/tennis/serena-williams-wins-first-title-
21263972
Section (first URL path / og:section) - e.g. Sports
Subsection (second URL path) - e.g. Tennins
Keywords (meta keywords) - e.g. Serena Williams,Caroline Wozniacki,Australian Open
Authors (meta article:author) - e.g. Hassan Rashed
Headline (og:title) - e.g. Serena Williams wins first title in three years at Auckland Classic
Publication date (article:published_time) - e.g. 2020 01 12T0751 06Z
Article body length - e.g. 1300 words
Useful libraries: https://newspaper.readthe"""