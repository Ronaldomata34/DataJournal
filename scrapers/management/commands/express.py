from django.core.management.base import BaseCommand, CommandError
from scrapers.spiders import TheExpress

class Command(BaseCommand):
    help = 'Run scraper'

    def handle(self, *args, **options):
        scraper = TheExpress()
        scraper.start_scraper()
        self.stdout.write(self.style.SUCCESS('Successfully scraped'))