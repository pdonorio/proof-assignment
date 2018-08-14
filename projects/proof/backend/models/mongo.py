# -*- coding: utf-8 -*-

"""
https://pymodm.readthedocs.io/en/0.4.0/getting-started.html#defining-models
"""
from difflib import SequenceMatcher

from pymodm import connect, MongoModel, fields
from pymodm.errors import ValidationError
from proof.apis import APP_DB


###############
# my custom models

#connect(APP_DB)


class Article(MongoModel):
    """
    Model example to work with Mongo DB

    List of possible fields
    https://pymodm.readthedocs.io/en/0.4.0/api/index.html#model-fields
    """
    url = fields.URLField(primary_key=True)
    title = fields.CharField()
    text = fields.CharField()
    source = fields.CharField()
    published_date = fields.DateTimeField()
    country_code = fields.CharField()
    authors = fields.ListField(field=fields.CharField())
    tags = fields.ListField(field=fields.CharField())
    similar_text_flag = fields.BooleanField()

    class Meta:
        connection_alias = APP_DB

    def clean(self):
        articles = Article.objects.all()
        for article in articles:
            if SequenceMatcher(None, self.title, article.title).ratio() >= 0.8:
                return ValidationError('Title is very similar to existing one')

            if SequenceMatcher(None, self.text, article.text).ratio() >= 0.9:
                self.similar_text_flag = True
