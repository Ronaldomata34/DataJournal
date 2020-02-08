from django.core.management.base import BaseCommand, CommandError
from scrapers.spiders import Metro

class Command(BaseCommand):
    help = 'Run scraper'

    def handle(self, *args, **options):
        scraper = Metro()
        scraper.start_scraper()
        self.stdout.write(self.style.SUCCESS('Successfully scraped'))