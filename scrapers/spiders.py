import requests
from bs4 import BeautifulSoup

from articles.models import Article, Source, SourceCategory

class TheGuardianSpider():
    URL = 'https://www.theguardian.com/sitemaps/news.xml'

    def start_scraper(self):
        request = requests.get(self.URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        articles = soup.find_all("url")
        for article in articles:
            item = {}
            item['url'] = article.find('loc').text
            item['publisher'] = article.find('news:news').find('news:publication').find('news:name').text
            item['headline'] = article.find('news:news').find('news:title').text
            item['keywords'] = article.find('news:news').find('news:keywords').text
            item['publication_date'] = article.find('news:news').find('news:publication_date').text
            more = requests.get(item['url'])
            #print(more.text)
            more_soup = BeautifulSoup(more.content, 'html.parser')
            x = more_soup.find("meta", {"name":"author"})
            item['author'] = x["content"] if x else None
            print(item['url'])
            try:
                ps = more_soup.find("div", {"itemprop":"articleBody"}).find_all('p')
                body = [x.text for x in ps]
                print(body)
                print(item)
            except:
                print("Error \n"*5)
            
            

"""WEBSITES = [
    'bcc-news',
    'cnn',
    'the-new-york-times',
    'the-washington-post',
    'cnbc',
    'the-wall-street-journal',
    'bloomberg',
]

class SourceSpider():
    API_KEY_NEWSAPI = "797611d6cac94558b5c88a62731e585d"

    def __init__(self):
        self.newsapi = NewsApiClient(api_key='b19f466dc0af42d89100f1ec16544e6f')

    def start_scraper(self):
        response = self.newsapi.get_sources()
        #print(sources)
        if response['status'] == 'ok':
            sources = response['sources']
            for source in sources:
                obj_category, created_category = SourceCategory.objects.get_or_create(
                    name=source['category']
                )
                obj_source, created_source = Source.objects.get_or_create(
                    slug = source['id'],
                    name = source['name'],
                    description = source['description'],
                    url = source['url'],
                    category = obj_category,
                    language = source['language'],
                    country = source['country'],
                )
                if not created_source:
                    sys.stdout.write("{} already in database \n".format(obj_source.name.encode("utf-8")))
                else:
                    sys.stdout.write("{} was added to the database \n".format(obj_source.name.encode("utf-8")))


class ArticleSpider():
    API_KEY_NEWSAPI = "797611d6cac94558b5c88a62731e585d"

    def __init__(self):
        self.newsapi = NewsApiClient(api_key='b19f466dc0af42d89100f1ec16544e6f')
    
    def get_num_of_pages(self, total_results):
        return math.ceil(total_results/20)

    def start_scraper(self):
        today = datetime.today()
        from_date = today - timedelta(days=1)
        today = today.strftime("%Y-%m-%d")
        from_date = from_date.strftime("%Y-%m-%d")
        items = Source.objects.filter(to_scrape=True)
        for item in items:
            response = self.newsapi.get_everything(
                sources=item.slug,
                from_param=from_date,
                to=today
            )
            if response['status'] == 'ok':
                num_of_pages = self.get_num_of_pages(response['totalResults'])

                for n in range(1,num_of_pages):
                    r = self.newsapi.get_everything(
                            sources=item.slug,
                            from_param=from_date,
                            to=today,
                            page=n
                    )
                    for w, article in enumerate(r['articles']):
                        print(w, article['source'])"""
        
        