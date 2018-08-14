# -*- coding: utf-8 -*-

from restapi.rest.definition import EndpointResource
from proof.apis import SERVICE_NAME
from flask_restful import reqparse, abort
from flask import jsonify
# from utilities import htmlcodes as hcodes
from utilities.logs import get_logger
from proof.apis.articleparser import ArticleParser
#from proof.models.mongo import Article
import validators
import en_core_web_sm

log = get_logger(__name__)



class Articles(EndpointResource):

    def get(self):
        """
        Get an article if requested,
        or the top 10 articles if no url is specified
        """

        log.info('Requesting article(s)')

        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, help='Article URL to check')
        args = parser.parse_args()

        # connect to mongo
        db = self.get_service_instance(SERVICE_NAME)

        if not args['url']:
            return str(list(db.Article.objects.limit(10).values()))



        # custom ODM models (like `Examples`) can be added in
        # projects/proof/backend/models/mongo.py
        # documentation for queries at:
        # https://pymodm.readthedocs.io/en/0.4.0
        #   /getting-started.html#accessing-data

        # you can safely return python built-in types
        # that can be encoded with the json library



        if db.Article.objects.raw({'url':args['url']}).count():
            return str(list(db.Article.objects.raw({'url':args['url']}).values()))
        else:
            return self.send_errors(
                message='The requested url was not found!'
            )


    def post(self):
        """
        Submit an article
        """

        log.info('Request: submitting an article for parsing')

        # Try to get input
        inputs = self.get_input()
        log.pp(inputs)

        if not 'url' in inputs or not inputs['url']:
            return self.send_errors(
                message='You must submit a url for parsing!'
            )

        if not validators.url(inputs['url']):
            return self.send_errors(
                message='Malformed url!'
            )

        db = self.get_service_instance(SERVICE_NAME)
        # to store data on mongo via ODM:
        # https://pymodm.readthedocs.io/en/0.4.0
        #   /getting-started.html#creating-data


        if db.Article.objects.raw({'url':inputs['url']}).count():
            return self.send_errors(
                message='This url has already been submitted!'
            )


        parsed = ArticleParser(inputs['url']).parse()

        db_article = db.Article(**parsed)

        # searching for similarity to all other currently stored articles using spacy/nlp
        nlp = en_core_web_sm.load()
        new_article = nlp(parsed['text'])
        for article in db.Article.objects.all():
            prev_article = nlp(article.text)
            if new_article.similarity(prev_article) > 0.98:
                db_article.similar_to.append(article._id)

        db_article.save()

        return 'Article Submitted!'
