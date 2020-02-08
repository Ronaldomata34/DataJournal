from django.core.management.base import BaseCommand, CommandError
from scrapers.spiders import TheGuardianSpider

class Command(BaseCommand):
    help = 'Run cars scraper'

    def handle(self, *args, **options):
        scraper = TheGuardianSpider()
        scraper.start_scraper()
        self.stdout.write(self.style.SUCCESS('Successfully scraped'))