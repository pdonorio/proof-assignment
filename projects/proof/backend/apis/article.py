# -*- coding: utf-8 -*-

from restapi.rest.definition import EndpointResource
from proof.apis import SERVICE_NAME
from proof.services.article_parser import parse_article
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

        if url:
            return mongo.Article.objects.get(url=url)

        # you can safely return python built-in types
        # that can be encoded with the json library
        articles = mongo.Article.objects.limit(10)
        return list(articles.values())

    def post(self):
        """
        Submit an article
        """

        log.info('Request: submitting an article for parsing')

        # Try to get input
        parameters = self.get_input()
        log.pp(parameters)

        url = parameters.get('URI')

        if not url:
            return self.send_errors(
                message='You must submit a url for parsing!'
            )

        article_data = parse_article(url)
        mongo = self.get_service_instance(SERVICE_NAME)
        article = mongo.Article(**article_data).save()

        return list(article)
