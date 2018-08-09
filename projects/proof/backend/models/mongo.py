# -*- coding: utf-8 -*-

import os
import json
from bson import ObjectId
from datetime import datetime
from pymodm import MongoModel, fields
from pymongo import MongoClient
from datetime import datetime
# from restapi.models.mongo import User
# from pymongo.write_concern import WriteConcern

MongoClient
APP_DB = os.environ.get('MONGO_DATABASE', 'unknown')


###############
# encoder to dump json for responses output in flask
class MongoObjectEncoder(json.JSONEncoder):
    def default(self, o):
        # print(o.__class__.__name__, type(o))
        # if o is None:
        #     return 'null'
        if isinstance(o, datetime):
            # return o.isoformat()
            return o.timestamp()
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, MongoModel):
            return o.__dict__.get('_data')
        return json.JSONEncoder.default(self, o)

###############
# my models

class Configuration(MongoModel):
    """ A possible collection to store configurations """
    key = fields.CharField(primary_key=True)
    value = fields.CharField()


class Examples(MongoModel):
    """ Model example to work with Mongo DB """
    name = fields.CharField(primary_key=True)
    truth = fields.BooleanField()  # Mostly True / Mostly False
    description = fields.CharField()
    created = fields.DateTimeField()
    value = fields.IntegerField(default=1)

    class Meta:
        connection_alias = APP_DB

class Articles(MongoModel):
    """ Simple article collection """
    url = fields.URLField(primary_key=True)
    submitted = fields.DateTimeField()
    created = fields.DateTimeField()
    ## can be multiple authors
    authors = fields.ListField(default=[])
    title = fields.CharField()
    text = fields.CharField()
    duplicate = fields.BooleanField()

    class Meta:
        connection_alias = APP_DB
    ## should eventually break text field up for easier comparisons

