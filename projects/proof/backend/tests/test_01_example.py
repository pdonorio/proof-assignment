# -*- coding: utf-8 -*-


from restapi.tests import BaseTests, API_URI  # , AUTH_URI
from utilities import htmlcodes as hcodes
from utilities.logs import get_logger
# import json
# from tests.custom import example_json_input
# from restapi.services.detect import detector
# from proof.models.mongo import MongoClient, APP_DB
# from proof.apis.quizzes import SERVICE_NAME

log = get_logger(__name__)

# #################
# # ## DROP DB
# extension = detector.services_classes.get(SERVICE_NAME)
# db = extension().get_instance()
# client = MongoClient(db.connection.conn_string)
# client.drop_database(APP_DB)


#################
class TestExamples(BaseTests):

    _main_endpoint = '/examples'

    def test_01_something(self, client):

        endpoint = API_URI + self._main_endpoint
        log.info('Testing GET examples')

        # set a list of URLs and loop
        urls = [
            'https://blabla/test'
        ]

        for url in urls:
            # If NO authorization required
            r = client.get(endpoint)
            # headers, _ = self.do_login(client, None, None)
            # r = client.get(
            #     endpoint,
            #     headers=headers  # If authorization required
            # )
            assert r.status_code == hcodes.HTTP_OK_BASIC

        # ####################
        # output = self.get_content(r)
        # assert output.get('status') == 'created'

        assert True
