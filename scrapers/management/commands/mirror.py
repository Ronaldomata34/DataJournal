from django.core.management.base import BaseCommand, CommandError
from scrapers.spiders import Mirror

class Command(BaseCommand):
    help = 'Run scraper'

    def handle(self, *args, **options):
        scraper = Mirror()
        scraper.start_scraper()
        self.stdout.write(self.style.SUCCESS('Successfully scraped'))