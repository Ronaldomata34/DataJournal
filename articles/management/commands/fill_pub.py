from django.core.management.base import BaseCommand, CommandError
from articles.models import Publisher

class Command(BaseCommand):
    help = 'fill publisher table (metadata)'

    def handle(self, *args, **options):
        sites = [
            {
                "name": "BBC News",
                "url": "https://www.bbc.co.uk/news",
                "country": "uk"
            },
            {
                "name": "The Guardian",
                "url": "https://www.theguardian.com",
                "country": "uk"
            },
            {
                "name": "The Daily Mail",
                "url": "https://www.dailymail.co.uk/",
                "country": "uk"
            },
            {
                "name": "The Times",
                "url": "https://www.thetimes.co.uk/",
                "country": "uk"
            },
            {
                "name": "The Sun",
                "url": "https://www.thesun.co.uk/",
                "country": "uk"
            },
            {
                "name": "The Daily Telegraph",
                "url": "https://www.telegraph.co.uk",
                "country": "uk"
            },
            {
                "name": "Daily Mirror",
                "url": "https://www.mirror.co.uk/",
                "country": "uk"
            },
            {
                "name": "Metro",
                "url": "https://metro.co.uk/",
                "country": "uk"
            },
            {
                "name": "Daily Express",
                "url": "https://www.express.co.uk/",
                "country": "uk"
            },
            {
                "name": "Daily Star",
                "url": "https://www.dailystar.co.uk/",
                "country": "uk"
            }
        ]
        for site in sites:
            model = Publisher(**site)
            model.save()
        self.stdout.write(self.style.SUCCESS('Ran it Successfully'))