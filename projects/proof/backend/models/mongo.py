# -*- coding: utf-8 -*-

"""
https://pymodm.readthedocs.io/en/0.4.0/getting-started.html#defining-models
"""

from proof.apis import APP_DB
from pymodm import MongoModel, fields


###############
# my custom models

class Examples(MongoModel):
    """
    Model example to work with Mongo DB

    List of possible fields
    https://pymodm.readthedocs.io/en/0.4.0/api/index.html#model-fields
    """
    name = fields.CharField(primary_key=True)
    truth = fields.BooleanField()  # Mostly True / Mostly False
    description = fields.CharField()
    created = fields.DateTimeField()
    value = fields.IntegerField(default=1)

    class Meta:
        connection_alias = APP_DB


class Article_M(MongoModel):
    url = fields.CharField(primary_key=True)
    title = fields.CharField()
    authors = fields.ListField(fields.CharField(), default=list)
    publish_date = fields.CharField()
    text = fields.CharField()
    keywords = fields.ListField(fields.CharField())
    summary = fields.CharField()
    source = fields.CharField()
    html = fields.CharField()
    ip = fields.CharField()
    city = fields.CharField()
    country = fields.CharField()
    region = fields.CharField()
    images = fields.ListField(fields.CharField(), default=list)
    movies = fields.ListField(fields.CharField(), default=list)
    flagged = fields.BooleanField(default=False)

    class Meta:
        connection_alias = APP_DB
