# -*- coding: utf-8 -*-

"""
https://pymodm.readthedocs.io/en/0.4.0/getting-started.html#defining-models
"""
import requests
import html2text

from lxml import html
from pymodm import MongoModel, fields

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
    author = fields.CharField(primary_key=True, blank=True)
    truth = fields.BooleanField(blank=True)  # Mostly True / Mostly False
    title = fields.CharField(unique=True, blank=True)
    text = fields.CharField(blank=True)
    date = fields.DateTimeField(blank=Trues)
    value = fields.IntegerField(default=1)
    url = fields.CharField()

    def save(self, *args, **kwargs):
        self.text = self.scrape_text()
        self.title = self.parse_title()
        self.author = self.parse_name()
        self.date = self.parse_date()
        super().save(*args, **kwargs)

    def scrape_text(self):
        webpage = requests.get(self.url)

    def parse_title(self):

    def parse_name(self):

    def parse_date(self):


    class Meta:
        connection_alias = APP_DB
