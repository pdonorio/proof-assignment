# -*- coding: utf-8 -*-
import requests

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
        url = inputs.get('url')

        if url is None:
            return self.send_errors(
                message='You must submit a url for parsing!', code=400
            )

        try:
            result = requests.head(url)
        except requests.exceptions.MissingSchema:
            return self.send_errors(
                message='The submitted url is not valid.', code=400
            )
        except requests.ConnectionError:
            return self.send_errors(
                message='Connection error occurred.', code=400
            )
        except requests.TooManyRedirects:
            return self.send_errors(
                message='To many redirects occurred.', code=400
            )
        except requests.Timeout:
            return self.send_errors(
                message='Connection time out.', code=400
            )
        except requests.HTTPError:
            return self.send_errors(
                message='A http error occurred.', code=400
            )

        log.info('Printing head')
        log.pp(result)

        # to store data on mongo via ODM:
        # https://pymodm.readthedocs.io/en/0.4.0
        #   /getting-started.html#creating-data

        return 'To be implemented'

    @staticmethod
    def is_valid_result(result):
        return result.status_code != 200
