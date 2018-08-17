# -*- coding: utf-8 -*-

"""
https://pymodm.readthedocs.io/en/0.4.0/getting-started.html#defining-models
"""
from BeautifulSoup import BeautifulSoup
from pymodm import MongoModel, fields
from urllib.request import urlopen

from proof.apis import APP_DB


###############
# my custom models

class ProofArticle(MongoModel):
    """
    Model example to work with Mongo DB

    List of possible fields
    https://pymodm.readthedocs.io/en/0.4.0/api/index.html#model-fields

    These fields are scraped and parsed from articles users post to Proof.
    """
    author = fields.CharField(primary_key=True)
    truth = fields.BooleanField(blank=True)  # Mostly True / Mostly False
    title = fields.CharField(unique=True)
    text = fields.CharField()
    date = fields.DateTimeField()
    value = fields.IntegerField(default=1)
    url = fields.URLField()

    class Meta:
        connection_alias = APP_DB

    def __init__(self, *args, **kwargs):
        self.text = self.scrape_text()
        self.title = self.parse_title()
        self.author = self.parse_name()
        self.date = self.parse_date()
        super().__init__(*args, **kwargs)

    def scrape_text(self):
        page = urllib.request.urlopen(self.url)
        html = webpage.read()
        page.close()
        soup = BeautifulSoup(html)
        scraped_text = ''.join(soup.findAll(text=True))
        return scraped_text

    def parse_title(self):
        page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(page)
        parse_title = soup.title.string
        return parse_title

    def parse_name(self):
       soup = BeautifulSoup(requests.get(s).content, 'html.parser')
       meta = soup.find('meta', {'name': 'byl'})
       parse_name = meta["content"]
       return parse_name

    def parse_date(self):
       soup = BeautifulSoup(requests.get(s).content, 'html.parser')
       meta = soup.find('meta', {'name': 'byl'})
       parse_date = meta["content"]
       return parse_date
