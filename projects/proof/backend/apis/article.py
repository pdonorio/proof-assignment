# -*- coding: utf-8 -*-

from flask import Flask, request
from restapi.rest.definition import EndpointResource
from proof.apis import SERVICE_NAME
# from utilities import htmlcodes as hcodes
from utilities.logs import get_logger

log = get_logger(__name__)
app = Flask(__name__)


class Articles(EndpointResource):

    # Make sure the form the user has posted to is designated for
    # querying the database
    @app.route('/app', methods=['GET'])
    def get(self):
        url = request.form.get('url')
        """
        Get an article if requested,
        or the top 10 articles if no url is specified
        """

        log.info('Requesting article(s)')

        # connect to mongo
        mongo = self.get_service_instance(SERVICE_NAME)
        log.debug('Mongo ODM handler: %s', mongo)

        # Check to see if the user left the form blank or input a url
        # TODO: validate if the user put in a valid url
        if url is None:
            return mongo.ProofArticle.objects.limit(10)
        else:
            return mongo.ProofArticle.objects.raw({"url"})

        # custom ODM models (like `Examples`) can be added in
        # projects/proof/backend/models/mongo.py
        # documentation for queries at:
        # https://pymodm.readthedocs.io/en/0.4.0
        #   /getting-started.html#accessing-data

        # you can safely return python built-in types
        # that can be encoded with the json library

    # Make sure that the user has submitted the article to the form designated
    # for creating new articles
    @app.route('/app', methods=['POST'])
    def post(self):
        """
        Submit an article
        """
        # Retrieve the url from the form
        # TODO: validate if the user put in a valid url
        url = request.form.get('url')

        log.info('Request: submitting an article for parsing')

        # Try to get input
        inputs = self.get_input()
        log.pp(inputs)

        # Check if url already exists against the database
        if mongo.Examples.objects.filter(url = cleaned_info['url']).exists():
            return self.send_errors(
                message='This article has already been submitted!'
            )
        elif url is None:
            return self.send_errors(
                message='You must submit a url for parsing!'
            )
        else:
            # Create a new mongo object based on the posted url
            mongo.ProofArticle.objects.create(url=self.url)

        # to store data on mongo via ODM:
        # https://pymodm.readthedocs.io/en/0.4.0
        #   /getting-started.html#creating-data
