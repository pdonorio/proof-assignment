# -*- coding: utf-8 -*-
import requests

from datetime import datetime
from difflib import SequenceMatcher

from restapi.rest.definition import EndpointResource
from proof.apis import SERVICE_NAME
from proof.apis.article_parser import ArticleParser
from utilities import htmlcodes as hcodes
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

        mongo.ArticleModel.objects.all()
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
        url = inputs.get('url')

        if url is None:
            return self.send_errors(
                message='You must submit a url for parsing!', code=hcodes.HTTP_BAD_REQUEST
            )

        # connect to mongo
        mongo = self.get_service_instance(SERVICE_NAME)

        article_qs = mongo.ArticleModel.objects.raw({"url": url})

        if article_qs.count() > 0:
            return self.send_errors(
                message='The provided url was already been submitted.', code=hcodes.HTTP_BAD_REQUEST
            )

        try:
            result = requests.head(url)
            if result.status_code != 200:
                raise requests.HTTPError
        except requests.exceptions.MissingSchema:
            return self.send_errors(
                message='The submitted url is not valid.', code=hcodes.HTTP_BAD_REQUEST
            )
        except requests.ConnectionError:
            return self.send_errors(
                message='Connection error occurred.', code=hcodes.HTTP_BAD_REQUEST
            )
        except requests.TooManyRedirects:
            return self.send_errors(
                message='To many redirects occurred.', code=hcodes.HTTP_BAD_REQUEST
            )
        except requests.Timeout:
            return self.send_errors(
                message='Connection time out.', code=hcodes.HTTP_BAD_REQUEST
            )
        except requests.HTTPError:
            return self.send_errors(
                message='A http error occurred.', code=hcodes.HTTP_BAD_REQUEST
            )

        article_parser = ArticleParser(url)

        # Check similarity between submitted article and existing articles
        check_text_similarity = self.has_similar_text_article(db_connection=mongo,
                                                              article_title=article_parser.get_title(),
                                                              article_text=article_parser.get_text())
        if check_text_similarity:
            return check_text_similarity

        mongo.ArticleModel(
            url=url,
            date=datetime.now(),
            text=article_parser.get_text(),
            title=article_parser.get_title(),
            tag=article_parser.get_tags(),
        ).save()

        return "Article created successfully"

    def has_similar_text_article(self, db_connection, article_title, article_text):
        """
        Check compare given article_title with each article title in the database.
        Check compare given article_text with each article text in the database.
        In case to find a similarity above 80% return a error
        Otherwise return False
        """
        for article_model in db_connection.ArticleModel.objects.all():
            # Compare article title
            article_title_ratio_similarity = SequenceMatcher(None, article_model.title, article_title).ratio()
            if article_title_ratio_similarity > 0.8:
                return self.send_errors(
                    message='An article with a very similar title was already submitted.',
                    code=hcodes.HTTP_BAD_REQUEST
                )

            # Compare article text
            article_text_ratio_similarity = SequenceMatcher(None, article_model.text, article_text).ratio()
            if article_text_ratio_similarity > 0.8:
                return self.send_errors(
                    message='An article with a very similar text was already submitted.',
                    code=hcodes.HTTP_BAD_REQUEST
                )

        return False
