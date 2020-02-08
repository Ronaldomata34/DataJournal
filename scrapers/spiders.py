import re

import datetime
import requests
import dateutil.parser
from bs4 import BeautifulSoup

from articles.models import Article, Publisher

class TheGuardianSpider():
    URL = 'https://www.theguardian.com/sitemaps/news.xml'

    def start_scraper(self):
        request = requests.get(self.URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        articles = soup.find_all("url")
        for article in articles:
            #From xml url
            item = {}
            item['url'] = article.find('loc').text
            item['publisher'] = Publisher.objects.get(name="The Guardian")
            item['headline'] = article.find('news:news').find('news:title').text
            item['keywords'] = article.find('news:news').find('news:keywords').text

            # Datetime parser
            publication_date_str = article.find('news:news').find('news:publication_date').text
            item['published_at'] = dateutil.parser.parse(publication_date_str)


            if "/live/" in item['url'] or '/gallery/' in item['url']:
                #ignoring live and gallery articles
                continue

            #printing next url

            more = requests.get(item['url'])
            more_soup = BeautifulSoup(more.content, 'html.parser')

            #Author
            x = more_soup.find("meta", {"name":"author"})
            item['author'] = x if x else None
            if not item['author']:
                item['author'] = more_soup.find("meta", {"property":"article:author"})
            if not item['author']:
                item['author'] = ''
            else:
                item['author'] = item['author'].attrs["content"]

            #get section and subsection
            lis = more_soup.find_all("li", {"class": "pillars__item"})
            item['section'] = self.get_current_section(lis)
            lis_subsection = more_soup.find_all("li", {"class": "subnav__item"})
            item['subsection'] = self.get_current_section(lis_subsection, sub=True)
            
            #try:
            body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))
            item['content'] = content
            item['content_length'] = counter
            model = Article(**item)
            model.save()
            item['content'] = ''
            print(item)
            """except Exception as e:
                #Sent message to telegram
                print(e)
                exit()"""
    
    def get_current_section(self, lis, sub=False):
        """
            return current section from li elements
        """
        if sub:
            for li in lis:
                #print(li.find('a')['class'])
                if "subnav-link--current-section" in li.find('a')['class']:
                    return li.find('a').text.strip().capitalize()
        else:
            for li in lis:
                #print(li.find('a')['class'])
                if "pillar-link--current-section" in li.find('a')['class']:
                    return li.find('a').text.strip().capitalize()
        return ''


class TheExpress():
    

    def __init__(self):
        date = datetime.datetime.now()
        month = date.month
        if month <= 9:
            month = "0"+str(month)
        else:
            month = str(month)
        self.URL = 'https://www.express.co.uk/news/uk/{year}{month}.xml'.format(year=date.year, month=month)

    def start_scraper(self):
        request = requests.get(self.URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        articles = soup.find_all("url")
        for article in articles:
            #From xml url
            item = {}
            item['url'] = article.find('loc').text
            item['publisher'] = Publisher.objects.get(name="Daily Express")



            if "/live/" in item['url'] or '/gallery/' in item['url']:
                #ignoring live and gallery articles
                continue

            #printing next url

            more = requests.get(item['url'])
            more_soup = BeautifulSoup(more.content, 'html.parser')
            print(item['url'])
            item['headline'] = more_soup.find('meta', {"property": "og:title"})['content']
            #Author
            item['author'] = more_soup.find("meta", {"name":"author"})['content']
            # Datetime parser
            publication_date_str = more_soup.find("meta", {"property":"article:published_time"})['content']
            item['published_at'] = dateutil.parser.parse(publication_date_str)

            #get section and subsection
            lis = more_soup.find("ul", {"class": "main-nav"}).find_all('li')
            item['section'] = self.get_current_section(lis)
            lis_subsection = more_soup.find("ul", {"class": "page sub-nav"}).find_all('li') 
            item['subsection'] = self.get_current_section(lis_subsection, sub=True)
            
            #try:
            item['content'] = ''
            item['content_length'] = more_soup.find('meta', {"property": "article:word_count"})['content']
            item['keywords'] = more_soup.find('meta', {"name": "news_keywords"})['content']
            model = Article(**item)
            model.save()
            """body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))"""
            print(item)
            """except Exception as e:
                #Sent message to telegram
                print(e)
                exit()"""

    def get_current_section(self, lis, sub=False):
        """
            return current section from li elements
        """
        if sub:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        else:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        return ''


class TheDailyMail():
    

    def __init__(self):
        date = datetime.datetime.now()
        month = date.month
        day = date.day
        if month <= 9:
            month = "0"+str(month)
        else:
            month = str(month)
        if day <= 9:
            day = "0"+str(day)
        else:
            day = str(day)
            
        self.URL = "https://www.dailymail.co.uk/sitemap-articles-day~{year}-{month}-{day}.xml".format(year=date.year, month=month, day=day)

    def start_scraper(self):
        request = requests.get(self.URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        articles = soup.find_all("url")
        for article in articles:
            #From xml url
            item = {}
            item['url'] = article.find('loc').text
            item['publisher'] = Publisher.objects.get(name="The Daily Mail")



            if "/live/" in item['url'] or '/gallery/' in item['url']:
                #ignoring live and gallery articles
                continue

            #printing next url

            more = requests.get(item['url'])
            more_soup = BeautifulSoup(more.content, 'html.parser')
            print(item['url'])
            item['headline'] = more_soup.find('meta', {"property": "og:title"})['content']
            #Author
            item['author'] = more_soup.find("meta", {"name":"author"})['content']
            # Datetime parser
            publication_date_str = more_soup.find("meta", {"property":"article:published_time"})['content']
            item['published_at'] = dateutil.parser.parse(publication_date_str)

            #get section and subsection
            item['section'] = more_soup.find("meta", {"property":"article:section"})['content']
            item['subsection'] = ''
            
            #try:
            item['keywords'] = more_soup.find('meta', {"name": "news_keywords"})['content']

            body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))
            item['content'] = content
            item['content_length'] = counter


            model = Article(**item)
            model.save()
            """body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))"""
            print(item)
            """except Exception as e:
                #Sent message to telegram
                print(e)
                exit()"""

    def get_current_section(self, lis, sub=False):
        """
            return current section from li elements
        """
        if sub:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        else:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        return ''


class TheDailyStar():
    URL = "https://www.dailystar.co.uk/map_news.xml"

    def start_scraper(self):
        request = requests.get(self.URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        articles = soup.find_all("url")
        for article in articles:
            #From xml url
            item = {}
            item['url'] = article.find('loc').text
            item['publisher'] = Publisher.objects.get(name="Daily Star")



            if "/live/" in item['url'] or '/gallery/' in item['url']:
                #ignoring live and gallery articles
                continue

            #printing next url

            more = requests.get(item['url'], headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            })
            more_soup = BeautifulSoup(more.content, 'html.parser')
            print(item['url'])
            item['headline'] = more_soup.find('meta', {"property": "og:title"})['content']
            #Author
            item['author'] = more_soup.find("meta", {"name":"author"})['content']
            # Datetime parser
            publication_date_str = more_soup.find("meta", {"property":"article:published_time"})['content']
            item['published_at'] = dateutil.parser.parse(publication_date_str)

            #get section and subsection
            nav = more_soup.find('nav', {'class': 'breadcrumbs breadcrumbs-news'})
            ol = nav.find('ol')
            lis = ol.find_all('li')
            if len(lis) == 2:
                item['section'] = lis[1].find('a').text
                item['subsection'] = ''
            elif len(lis) == 3:
                item['subsection'] = lis[-1].find('a').text
                item['section'] = lis[-2].find('a').text
            else:
                item['subsection'] = lis[-2].find('a').text
                item['section'] = lis[-3].find('a').text

            
            #try:
            item['keywords'] = more_soup.find('meta', {"name": "news_keywords"})['content']

            body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))
            item['content'] = content
            item['content_length'] = counter


            model = Article(**item)
            model.save()
            """body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))"""
            print(item)
            """except Exception as e:
                #Sent message to telegram
                print(e)
                exit()"""

    def get_current_section(self, lis, sub=False):
        """
            return current section from li elements
        """
        if sub:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        else:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        return ''


class Metro():
    
    def __init__(self):
        date = datetime.datetime.now()
        month = date.month
        day = date.day
        if month <= 9:
            month = "0"+str(month)
        else:
            month = str(month)
        if day <= 9:
            day = "0"+str(day)
        else:
            day = str(day)
        self.URL = "https://metro.co.uk/sitemap.xml?yyyy={year}&mm={month}&dd={day}".format(year=date.year, month=month, day=day)

    def start_scraper(self):
        request = requests.get(self.URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        articles = soup.find_all("url")
        for article in articles:
            #From xml url
            item = {}
            item['url'] = article.find('loc').text
            item['publisher'] = Publisher.objects.get(name="Metro")



            if "/live/" in item['url'] or '/gallery/' in item['url']:
                #ignoring live and gallery articles
                continue

            #printing next url

            more = requests.get(item['url'], headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            })
            more_soup = BeautifulSoup(more.content, 'html.parser')
            print(item['url'])
            item['headline'] = more_soup.find('h1', {"class": "post-title clear"}).text
            #Author
            item['author'] = more_soup.find("a", {"rel":"author"}).text
            # Datetime parser
            publication_date_str = more_soup.find("meta", {"property":"article:published_time"})['content']
            item['published_at'] = dateutil.parser.parse(publication_date_str)

            #get section and subsection
            item['section'] = more_soup.find("meta", {"property":"article:section"})['content']
            item['subsection'] = ''
        

            
            #try:
            item['keywords'] = more_soup.find('meta', {"name": "news_keywords"})
            if item['keywords']:
                item['keywords'] = item['keywords']['content']
            else:
                item['keywords'] = ''

            body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"article-body"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))
            item['content'] = content
            item['content_length'] = counter


            model = Article(**item)
            model.save()
            """body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))"""
            print(item)
            """except Exception as e:
                #Sent message to telegram
                print(e)
                exit()"""

    def get_current_section(self, lis, sub=False):
        """
            return current section from li elements
        """
        if sub:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        else:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        return ''


class Mirror():
    URL = "https://www.mirror.co.uk/map_news.xml"

    def start_scraper(self):
        request = requests.get(self.URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        articles = soup.find_all("url")
        for article in articles:
            #From xml url
            item = {}
            item['url'] = article.find('loc').text
            item['publisher'] = Publisher.objects.get(name="Daily Mirror")
            item['headline'] = article.find('news:news').find('news:title').text
            publication_date_str = article.find('news:news').find('news:publication_date').text
            item['published_at'] = dateutil.parser.parse(publication_date_str)

            if "/live/" in item['url'] or '/gallery/' in item['url']:
                #ignoring live and gallery articles
                continue

            #printing next url

            more = requests.get(item['url'], headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            })
            more_soup = BeautifulSoup(more.content, 'html.parser')
            print(item['url'])
            #Author
            item['author'] = more_soup.find("meta", {"name":"author"})['content']
            # Datetime parser

            #get section and subsection
            nav = more_soup.find('nav', {'class': 'breadcrumbs'})
            ol = nav.find('ol')
            lis = ol.find_all('li')
            if len(lis) == 2:
                item['section'] = lis[1].find('a').text
                item['subsection'] = ''
            elif len(lis) == 3:
                item['subsection'] = lis[-1].find('a').text
                item['section'] = lis[-2].find('a').text
            else:
                item['subsection'] = lis[-1].find('a').text
                item['section'] = lis[-2].find('a').text
        

            
            #try:
            item['keywords'] = more_soup.find('meta', {"name": "news_keywords"})
            if item['keywords']:
                item['keywords'] = item['keywords']['content']
            else:
                item['keywords'] = ''

            body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"article-body"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))
            item['content'] = content
            item['content_length'] = counter


            model = Article(**item)
            model.save()
            """body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))"""
            print(item)
            """except Exception as e:
                #Sent message to telegram
                print(e)
                exit()"""

    def get_current_section(self, lis, sub=False):
        """
            return current section from li elements
        """
        if sub:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        else:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        return ''


class TheSun():
    
    def __init__(self):
        date = datetime.datetime.now()
        month = date.month
        day = date.day
        if month <= 9:
            month = "0"+str(month)
        else:
            month = str(month)
        if day <= 9:
            day = "0"+str(day)
        else:
            day = str(day)
        self.URL = "https://www.thesun.co.uk/sitemap.xml?yyyy={year}&mm={month}&dd={day}".format(year=date.year, month=month, day=day)

    def start_scraper(self):
        request = requests.get(self.URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        articles = soup.find_all("url")
        for article in articles:
            #From xml url
            item = {}
            item['url'] = article.find('loc').text
            item['publisher'] = Publisher.objects.get(name="The Sun")



            if "/live/" in item['url'] or '/gallery/' in item['url']:
                #ignoring live and gallery articles
                continue

            #printing next url

            more = requests.get(item['url'], headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            })
            more_soup = BeautifulSoup(more.content, 'html.parser')
            print(item['url'])
            item['headline'] = more_soup.find('h1', {"class": "article__headline"}).text
            #Author
            item['author'] = more_soup.find("span", {"class":"article__author-name"}).text
            # Datetime parser
            publication_date_str = more_soup.find("meta", {"property":"article:published_time"})['content']
            item['published_at'] = dateutil.parser.parse(publication_date_str)

            #get section and subsection
            ul = more_soup.find('ul', {'id': 'sun-men'})
            lis = ul.find_all('li')
            item['section'] = self.get_current_section(lis)
            ul_sub = more_soup.find("ul", {"class": "swiper-wrapper sub-nav__list"})
            lis_subsection = ul_sub.find_all('li')
            item['subsection'] = self.get_current_section(lis_subsection, sub=True)
        

            
            #try:
            item['keywords'] = more_soup.find('meta', {"name": "news_keywords"})
            if item['keywords']:
                item['keywords'] = item['keywords']['content']
            else:
                item['keywords'] = ''

            body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"article-body"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"article__content"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))
            item['content'] = content
            item['content_length'] = counter


            model = Article(**item)
            model.save()
            """body_content = more_soup.find("div", {"itemprop":"articleBody"})
            if not body_content:
                body_content = more_soup.find("div", {"itemprop":"reviewBody"})
            if not body_content:
                body_content = more_soup.find("div", {"class":"content__standfirst"})
            ps = body_content.find_all('p')
            body = [x.text for x in ps]
            content = ' '.join(body)
            counter = len(re.findall(r'\w+', content))"""
            print(item)
            """except Exception as e:
                #Sent message to telegram
                print(e)
                exit()"""

    def get_current_section(self, lis, sub=False):
        """
            return current section from li elements
        """
        if sub:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        else:
            for li in lis:
                #print(li.find('a')['class'])
                if "active" in li['class']:
                    return li.find('a').text.strip().capitalize()
        return ''





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
        
"""
content content--article content--pillar-news content--type-article section-australia-news tonal tonal--tone-news

content content--article content--pillar-sport content--type-feature section-football tonal tonal--tone-feature

content content--liveblog tonal tonal--tone-live blog is-live section-football content--pillar-sport content--has-scores

content content--article content--pillar-news content--type-article section-politics tonal tonal--tone-news

content content--article content--pillar-news content--type-article section-us-news tonal tonal--tone-news

content content--article content--pillar-lifestyle content--type-feature section-life-and-style tonal tonal--tone-feature

"""