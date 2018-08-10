# -*- coding: utf-8 -*-

from restapi.tests import BaseTests, API_URI
from utilities import htmlcodes as hcodes
from utilities.logs import get_logger

log = get_logger(__name__)


class TestArticle(BaseTests):

    """ Quickstart:
    - one method inside this class for each functionality to test
    - decide the order with the name: test_NUMBER_METHOD_FUNCTIONALITY
    """

    _main_endpoint = '/articles'

    def test_01_GET_giveityourname(self, client):
        """
        testing a feature on your endpoint class
        """

        endpoint = API_URI + self._main_endpoint
        log.info('*** Testing GET call on %s' % endpoint)

        # call the method `get`
        r = client.get(endpoint)
        # Assert what is right or wrong
        assert r.status_code == hcodes.HTTP_OK_BASIC

        # helper function to parse the standard output from rapydo flask server
        output = self.get_content(r)
        # pretty print data obtained from API to check the content
        log.pp(output)
        # check if the content is what you expect
        assert output == 'To be implemented'
