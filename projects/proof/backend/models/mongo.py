# -*- coding: utf-8 -*-

"""
https://pymodm.readthedocs.io/en/0.4.0/getting-started.html#defining-models
"""

from pymodm import MongoModel, fields
from proof.apis import APP_DB


###############
# my custom models


class Article(MongoModel):
    """
    Model example to work with Mongo DB

    List of possible fields
    https://pymodm.readthedocs.io/en/0.4.0/api/index.html#model-fields
    """
    #_id = fields.ObjectIdField(primary_key=True)
    truth = fields.BooleanField()  # Mostly True / Mostly False
    created = fields.DateTimeField(blank=True)
    url = fields.URLField()
    authors = fields.ListField(field=fields.CharField(), blank=True)
    date = fields.DateTimeField(blank=True)
    source = fields.CharField(blank=True)
    tags = fields.ListField(field=fields.CharField(), blank=True)
    location = fields.PointField(blank=True)
    title = fields.CharField(blank=True)
    text = fields.CharField(blank=True)
    abstract = fields.CharField(blank=True)
    keywords = fields.ListField(field=fields.CharField(), blank=True)
    similar_to = fields.ListField(field=fields.ObjectIdField(), blank=True)

    class Meta:
        connection_alias = APP_DB
