# -*- coding: utf-8 -*-
import json
import requests

from restapi.tests import BaseTests, API_URI
from utilities import htmlcodes as hcodes
from utilities.logs import get_logger
from unittest.mock import patch

log = get_logger(__name__)


class TestArticle(BaseTests):

    """ Quickstart:
    - one method inside this class for each functionality to test
    - decide the order with the name: test_NUMBER_METHOD_FUNCTIONALITY
    """

    _main_endpoint = API_URI + '/articles'

    def test_1_post_return_error_to_none_urls(self, client):
        """
        testing when user does not provide url.
        """

        # call the method `post`
        r = client.post(self._main_endpoint, data={'url': None})
        data = json.loads(r.data)
        # Asserts
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        assert data['Response']['errors'] == ['You must submit a url for parsing!']

    def test_2_post_return_error_to_invalids_urls(self, client):
        """
        testing when user does not provide a valid url.
        """

        # call the method `post`
        r = client.post(self._main_endpoint, data={'url': 'my invalid url'})
        data = json.loads(r.data)
        # Asserts
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        assert data['Response']['errors'] == ['The submitted url is not valid.']

    @patch("requests.head", autospec=True)
    def test_3_post_a_connection_error_occurred(self, mock, client):
        """
        testing when connection with page give a connection error.
        """
        mock.side_effect = requests.ConnectionError()

        # call the method `post`
        r = client.post(self._main_endpoint, data={'url': 'https://google.com'})
        data = json.loads(r.data)
        # Asserts
        mock.assert_called_once_with('https://google.com')
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        assert data['Response']['errors'] == ['Connection error occurred.']

    @patch("requests.head")
    def test_4_post_to_many_redirects_occurred(self, mock, client):
        """
        testing when connection with page returns to many redirects.
        """
        mock.side_effect = requests.TooManyRedirects()

        # call the method `post`
        r = client.post(self._main_endpoint, data={'url': 'https://google.com'})
        data = json.loads(r.data)
        # Asserts
        mock.assert_called_once_with('https://google.com')
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        assert data['Response']['errors'] == ['To many redirects occurred.']

    @patch("requests.head")
    def test_5_post_time_out_connection(self, mock, client):
        """
        testing when connection with page return time out.
        """
        mock.side_effect = requests.Timeout()

        # call the method `post`
        r = client.post(self._main_endpoint, data={'url': 'https://google.com'})
        data = json.loads(r.data)
        # Asserts
        mock.assert_called_once_with('https://google.com')
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        assert data['Response']['errors'] == ['Connection time out.']

    @patch("requests.head")
    def test_6_post_http_error_occurred(self, mock, client):
        """
        testing when connection with page return a http error.
        """
        mock.side_effect = requests.HTTPError()

        # call the method `post`
        r = client.post(self._main_endpoint, data={'url': 'https://google.com'})
        data = json.loads(r.data)
        # Asserts
        mock.assert_called_once_with('https://google.com')
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        assert data['Response']['errors'] == ['A http error occurred.']
