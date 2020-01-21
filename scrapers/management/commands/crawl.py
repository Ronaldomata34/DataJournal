from django.core.management.base import BaseCommand, CommandError
from scrapers.spiders import ArticleSpider

class Command(BaseCommand):
    help = 'Run cars scraper'

    def handle(self, *args, **options):
        scraper = ArticleSpider()
        scraper.start_scraper()
        self.stdout.write(self.style.SUCCESS('Successfully scraped'))