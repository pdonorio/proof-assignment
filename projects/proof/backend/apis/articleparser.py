from newspaper import Article
from utilities.logs import get_logger
from bs4 import BeautifulSoup
from dateutil.parser import parse as dateparse
from geotext import GeoText
from geopy import geocoders
from geojson import Point

log = get_logger(__name__)



class ArticleParser():

    def __init__(self, url):
        self.article = Article(url, language='en')
        self.article.download()
        self.results = {'authors': [],
                        'date': None,
                        'source': None,
                        'tags': [],
                        'location': None,
                        'title': None,
                        'text': None,
                        'abstract': None,
                        'keywords': [],
                        'url':url}
        self.parsed_html = None

    def parse(self):
        """
        Uses the newspaper library to do some automated parsing to fill in all the results fields
        For fields which are not determined, we try to use some direct html parsing and searching for the data
        In this exercise I have just tried to look at a number of random news sites and match based on them,
        however, the location of the relevant data should really be stored in the database if I was making a real app
        """

        self.article.parse()
        self.article.nlp()
        self.parsed_html = BeautifulSoup(self.article.html, 'html.parser')

        if self.article.authors:
            self.results['authors'] = self.article.authors
        else:
            pass

        if self.article.publish_date:
            self.results['date'] = self.article.publish_date
        else:
            self.results['date'] = self._find_date()

        # find source
        self.results['source'] = self._find_source()

        if self.article.tags:
            self.results['tags'] = self.article.tags
        else:
            self.results['tags'] = self._find_tags()

        if self.article.title:
            self.results['title'] = self.article.title


        if self.article.text:
            self.results['text'] = self.article.text
            # find location

        self.results['location'] = self._find_location()

        if self.article.keywords:
            self.results['keywords'] = self.article.keywords

        if self.article.summary:
            self.results['abstract'] = self.article.summary


        return self.results

    def _find_authors(self):
        pass

    def _find_date(self):

        for element_possibility in ({'class_': 'timestamp'},
                                    {'class_': 'date'},):
            dte = self.parsed_html.find(**element_possibility)
            if dte and dte.get_text():
                dte = self._parse_date(dte.get_text())
                if dte:
                    return dte


    def _find_source(self):
        for element_possibility in ({'property': 'og:site_name'},):
            source = self.parsed_html.find(**element_possibility)
            if source and source.get('content', None):
                return source['content']

    def _find_tags(self):

        tags = []
        search = self.parsed_html.find(class_="tags-list")
        if search and search.find_all('a'):
            for elem in search.find_all('a'):
                tags.append(elem.get_text())

        return tags

    def _find_location(self):
        """
        Find names of cities or countries in the title or text of the article,
        if found, look up the coordinates of the place and return it as a tuple
        """
        places = GeoText(' '.join((self.results.get('title', ''), self.results.get('text', ''))))

        gn = geocoders.GeoNames(username='sona1111')
        if places.cities:
            return Point(gn.geocode(places.cities[0])[1])
        elif places.country_mentions:
            return Point(gn.geocode(places.country_mentions[0][0])[1])



    def _parse_date(self, string):
        try:
            return dateparse(string)
        except ValueError:
            return None


if __name__ == "__main__":

    """
    nltk.download('punkt')    
    """

    urls = ['https://abcnews.go.com/Politics/white-house-exploring-legal-options-omarosa-manigault-newman/story?id=57146994',
            'http://www.foxnews.com/us/2018/08/13/crash-on-interstate-5-in-california-leads-to-fight-two-drivers-dying-police-say.html',
            'https://people.com/tv/jinger-duggar-surprises-family-pregnancy/',
            'https://www.bbc.com/news/world-us-canada-45177314',
            'http://www.nydailynews.com/news/crime/ny-news-stand-your-ground-florida-20180813-story.html']

    for url in urls:

        a = ArticleParser(url)

        log.pp(a.parse())
