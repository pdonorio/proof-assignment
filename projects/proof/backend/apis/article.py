# -*- coding: utf-8 -*-

from restapi.rest.definition import EndpointResource
from proof.apis import SERVICE_NAME
# from utilities import htmlcodes as hcodes
from utilities.logs import get_logger

log = get_logger(__name__)


class Articles(EndpointResource):

    def get(self, url=None):
        """
        Get an article if requested,
        or the top 10 articles if no url is specified
        """

        log.info('Requesting article(s)')

        # connect to mongo
        mongo = self.get_service_instance(SERVICE_NAME)
        log.debug('Mongo ODM handler: %s', mongo)

        mongo.Examples.objects.all()
        # custom ODM models (like `Examples`) can be added in
        # projects/proof/backend/models/mongo.py
        # documentation for queries at:
        # https://pymodm.readthedocs.io/en/0.4.0
        #   /getting-started.html#accessing-data

        # you can safely return python built-in types
        # that can be encoded with the json library
        return 'To be implemented'

    def post(self):
        """
        Submit an article
        """

        log.info('Request: submitting an article for parsing')

        # Try to get input
        inputs = self.get_input()
        log.pp(inputs)

        # if url is None:
        #     return self.send_errors(
        #         message='You must submit a url for parsing!'
        #     )

        # to store data on mongo via ODM:
        # https://pymodm.readthedocs.io/en/0.4.0
        #   /getting-started.html#creating-data

        return 'To be implemented'
