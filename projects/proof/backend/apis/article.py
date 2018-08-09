# -*- coding: utf-8 -*-

import json
from proof.models.mongo import MongoObjectEncoder
from restapi.rest.definition import EndpointResource
from utilities.logs import get_logger
from newspaper import Article as newspaperArticle
from datetime import datetime
from pytz import utc
# from restapi.services.detect import detector
# from utilities import htmlcodes as hcodes

log = get_logger(__name__)
SERVICE_NAME = "mongo"

# TODO: isolate the mongo connector so we don't copy the code a million times

class Articles(EndpointResource):

    def get(self, url=None):
        """ Get an article, or the top 20 article if no arg. Returns """

        log.info('Request: getting article after parsing')

        # connect to mongo
        mongo = self.get_service_instance(SERVICE_NAME)
        if mongo is None:
            log.error('Service %s unavailable', SERVICE_NAME)
            return self.send_errors(
                message='Server internal error. Please contact support.',
                # code=hcodes.HTTP_BAD_NOTFOUND
            )
        else:
            log.verbose("Connected to %s:\n%s", SERVICE_NAME, mongo)


        if url is None:
            cursor = mongo.Articles.objects.raw({})
            data_str = json.dumps(list(cursor), cls=MongoObjectEncoder)
            return json.loads(data_str)

        else:
            cursor = mongo.Articles.objects.raw({'url': url})
            data_str = json.dumps(list(cursor), cls=MongoObjectEncoder)
            return json.loads(data_str)

    def post(self, url=None):

        log.info('Request: submitting an article for parsing')

        inputs = self.get_input()
        # log.pp(inputs)
        url = inputs.get('URI', 'http://yourdefault.io')

        ## TODO, get url from POST data
        url = 'http://bbc.com/news/technology-44965154'

        # check url was submitted
        if url is None:
            return self.send_errors(
                message='You must submit a url for parsing!'
            )

        # connect to mongo
        mongo = self.get_service_instance(SERVICE_NAME)
        if mongo is None:
            log.error('Service %s unavailable', SERVICE_NAME)
            return self.send_errors(
                message='Server internal error. Please contact support.',
                # code=hcodes.HTTP_BAD_NOTFOUND
            )
        else:
            log.very_verbose("Connected to %s:\n%s", SERVICE_NAME, mongo)

        success, error_msg = self.parse_article(mongo, url)

        if success:
            log.verbose("Article has been inserted into datbase")
        else:
            log.verbose("Article was a duplicate!")

        return {'success': success, 'msg': error_msg}

    def parse_article(self, mongo_instance, url):
        """ Helper function to parse URL. Returns (bool, string) """

        article = newspaperArticle(url)

        ## verify that the article has been inserted into the database
        try:
            this_article = mongo_instance.Articles.objects.raw({})
        except:
            ## specify error
            return False, "Database error, please contact support!"

        for art in this_article:
            if art.url == url:
                return False, "This article has already been submitted into the database!"

        try:
            article.download()
        except:
            ## specify error
            return False, "Article could not be downloaded from server!"

        article.parse()

        create_date = article.publish_date
        if create_date is None:
            create_date=datetime.now()
        authors = article.authors
        if authors == []:
            authors = ['unknown']
        title = article.title
        text = article.text

        duplicate = self.check_for_duplicates(mongo_instance, text)

        try:
            mongo_instance.Articles(
                url=url,
                submitted=str(datetime.now(utc)),
                created=str(create_date),
                authors=authors,
                title=title,
                text=text,
                duplicate=duplicate
            ).save()
        except:
            ## specify error
            return False, "Database error, please contact support!"

        ## article has been parsed and inserted into database
        return True, ""

    def check_for_duplicates(self, mongo_instance, this_text):
        ## for article in db, convert texts to set, and do jaccard similarity test
        TOO_SIMILAR_RATIO = 0.9

        this_text_set = set(this_text.split())

        for record in mongo_instance.Articles.objects.raw({}):
            compare_text_set = set(record.text.split())

            intersect_sets = this_text_set.intersection(compare_text_set)

            ratio = float(len(intersect_sets) / (len(this_text_set) + len(compare_text_set) - len(intersect_sets)))
            print('ratio', ratio)

            if (ratio > TOO_SIMILAR_RATIO):

                return True

        ## this article is not a duplicate
        return False



