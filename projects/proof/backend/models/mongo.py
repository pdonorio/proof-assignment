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
    name = fields.CharField(primary_key=True)
    truth = fields.BooleanField()  # Mostly True / Mostly False
    description = fields.CharField()
    created = fields.DateTimeField()
    value = fields.IntegerField(default=1)

    class Meta:
        connection_alias = APP_DB
