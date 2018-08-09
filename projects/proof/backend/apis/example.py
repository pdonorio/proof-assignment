# -*- coding: utf-8 -*-

import json
from proof.models.mongo import MongoObjectEncoder
from restapi.rest.definition import EndpointResource
from utilities.logs import get_logger
# from datetime import datetime
# from pytz import utc
# from restapi.services.detect import detector
# from utilities import htmlcodes as hcodes

log = get_logger(__name__)
SERVICE_NAME = "mongo"


class Examples(EndpointResource):

    def get(self, example_id=None):

        ###########
        log.info("Request: %s", example_id)

        ###########
        # connect to mongo
        mongo = self.get_service_instance(SERVICE_NAME)
        if mongo is None:
            log.error('Service %s unavailable', SERVICE_NAME)
            return self.send_errors(
                message='Server internal error. Please contact adminers.',
                # code=hcodes.HTTP_BAD_NOTFOUND
            )
        else:
            log.very_verbose("Connected to %s:\n%s", SERVICE_NAME, mongo)

        ###########
        # QUERY ALL
        cursor = mongo.Examples.objects.raw({})
        data_str = json.dumps(list(cursor), cls=MongoObjectEncoder)
        return json.loads(data_str)

    def post(self):

        log.info("Request: submitting an example")

        # # connect to mongo
        # mongo = self.get_service_instance(SERVICE_NAME)
        # if mongo is None:
        #     log.error('Service %s unavailable', SERVICE_NAME)
        #     return self.send_errors(
        #         message='Server internal error. Please contact adminers.',
        #         # code=hcodes.HTTP_BAD_NOTFOUND
        #     )
        # else:
        #     log.very_verbose("Connected to %s:\n%s", SERVICE_NAME, mongo)

        return "To be implemented!"
