# -*- coding: utf-8 -*-

"""
https://pymodm.readthedocs.io/en/0.4.0/getting-started.html#defining-models
"""

from pymodm import MongoModel, fields
from proof.apis import APP_DB


###############
# my custom models

class Examples(MongoModel):
    """
    Model example to work with Mongo DB

    List of possible fields
    https://pymodm.readthedocs.io/en/0.4.0/api/index.html#model-fields
    """
    url = fields.URLField()
    date = fields.DateTimeField()
    author = fields.CharField(max_length=250)
    text = fields.CharField(max_length=5000)
    tag = fields.CharField(max_length=100)
    created = fields.DateTimeField()

    class Meta:
        connection_alias = APP_DB
