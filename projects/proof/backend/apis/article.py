# -*- coding: utf-8 -*-

import json
from difflib import SequenceMatcher
from urllib.parse import urlparse

# MY imports
import pymodm.errors
import pymongo
import requests
from flask import request
from newspaper import Article
from proof.apis import SERVICE_NAME
from restapi.rest.definition import EndpointResource
from utilities.logs import get_logger

log = get_logger(__name__)


class Articles(EndpointResource):

    def get(self):
        """
        Get an article if requested,
        or the top 10 articles if no url is specified
        """

        log.info('Requesting article(s)')

        # connect to mongo
        mongo = self.get_service_instance(SERVICE_NAME)
        log.debug('Mongo ODM handler: %s', mongo)

        try:
            # If the url variable is passed on the GET request return only the one article.
            inputs = self.get_input()
            url = inputs['url']
            # Does the url exist in our database?
            try:
                data = mongo.Article_M.objects.get({'_id': url}).to_son()
            except pymodm.errors.DoesNotExist:
                return self.send_errors(message='The url you entered does not exist in our database.')

        except KeyError:
            # If url isn't passed return top 10 as determined by the limit function.
            data = list(mongo.Article_M.objects.values().all().limit(10))

        return json.dumps(data, default=str)

    def post(self):
        """
        Submit an article
        """

        log.info('Request: submitting an article for parsing')
        # connect to mongo
        mongo = self.get_service_instance(SERVICE_NAME)

        # Try to get input
        try:
            inputs = self.get_input()
            url = inputs['url']
        except KeyError:
            return self.send_errors(message='You must submit a url for parsing!')

        # Use the newspaper library to get all the scraped info.
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        # Get the base url
        parsed_uri = urlparse(url)
        origin = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        data = requests.get("http://ipinfo.io/json").json()
        flagged = False
        # Check for plagiarism. Very inefficient. Using indexes will make this a lot faster probably.
        for art in mongo.Article_M.objects.all():
            title_ratio = SequenceMatcher(None, art.title, article.title).ratio()
            if title_ratio > 0.95:
                return self.send_errors(message='An article with a very similar title has already been posted.')
            text_ratio = SequenceMatcher(None, art.text, article.text).ratio()
            if text_ratio > 0.8:
                # We don't inform the user of his transgression.
                flagged = True
                break

        # Save to database if not already in there.
        art_obj = self.save_to_db(article, mongo, origin, data, url, flagged)

        return art_obj.to_son()

    def save_to_db(self, article, mongo, origin, data, url, flagged):
        """ Save to database if it doesn't exit already."""
        # Check for empty lists
        authors, movies, images, keywords = self.determine_if_lists_are_empty(article)
        try:
            art_obj = mongo.Article_M(url=url, title=article.title, authors=authors, publish_date=article.publish_date,
                                      text=article.text, keywords=keywords, summary=article.summary, source=origin,
                                      movies=movies, images=images, ip=request.remote_addr, city=data['city'],
                                      country=data['country'], region=data['region'], flagged=flagged).save(
                force_insert=True)
        except pymongo.errors.DuplicateKeyError:
            return self.send_errors(message='This article already exists.')
        return art_obj

    @staticmethod
    def determine_if_lists_are_empty(article):
        """ Determine if the lists returned by the newspaper library are empty.
        If they are, we pass a default not found string to the database."""
        if not article.authors:
            authors = ['Not Found.']
        else:
            authors = article.authors
        if not article.keywords:
            keywords = ['Not Found.']
        else:
            keywords = article.keywords
        if not article.images:
            images = ['Not Found.']
        else:
            images = article.images
        if not article.movies:
            movies = ['Not Found.']
        else:
            movies = article.authors

        return authors, movies, images, keywords
