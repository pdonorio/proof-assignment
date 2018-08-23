# -*- coding: utf-8 -*-
import json
import requests

from proof.models.mongo import ArticleModel
from restapi.tests import BaseTests, API_URI
from utilities import htmlcodes as hcodes
from utilities.logs import get_logger
from unittest.mock import patch

log = get_logger(__name__)

test_file = open("tests/custom/test_article.html").read()


class MockResponse(object):

    def __init__(self):
        self.status_code = 200
        self.content = test_file


class TestArticle(BaseTests):

    """ Quickstart:
    - one method inside this class for each functionality to test
    - decide the order with the name: test_NUMBER_METHOD_FUNCTIONALITY
    """

    _main_endpoint = API_URI + '/articles'

    @staticmethod
    def clean_existing_elements():
        ArticleModel.objects.all().delete()

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

    @patch("requests.get")
    @patch("requests.head")
    def test_7_post_add_new_article(self, mock_head, mock_get, client):
        """
        testing when adding a new article.
        """
        self.clean_existing_elements()
        mock_get.return_value = MockResponse()
        mock_head.return_value = MockResponse()

        # call the method `post`
        client.post(self._main_endpoint, data={'url': 'http://newsfromnyt.com'})

        # Db query
        article_qs = ArticleModel.objects.raw({"url": 'http://newsfromnyt.com'})

        # Assert
        mock_get.assert_called_once_with('http://newsfromnyt.com')
        assert article_qs.count() == 1
        article_qs = article_qs.first()
        assert article_qs.title == "The Unlikely Activists Who Took On Silicon" \
                                   " Valley — and Won - The New York Times"
        assert article_qs.tag == "Mactaggart"

    @patch("requests.get")
    @patch("requests.head")
    def test_8_post_ignore_article_with_almost_same_title(self, mock_head, mock_get, client):
        """
        testing when adding a new article.
        """
        self.clean_existing_elements()
        mock_get.return_value = MockResponse()
        mock_head.return_value = MockResponse()
        client.post(self._main_endpoint, data={'url': 'http://newsfromnyt.com'})

        # Edit Article to have almost same title
        article = ArticleModel.objects.get({"url": 'http://newsfromnyt.com'})
        article.title += '-'
        article.save()

        # call the method `post`
        r = client.post(self._main_endpoint, data={'url': 'http://mydifferentcity.com'})
        data = json.loads(r.data)

        # Db query
        article_qs = ArticleModel.objects.raw({"url": 'http://mydifferentcity.com'})

        # Assert
        assert article_qs.count() == 0
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        assert data['Response']['errors'] == ['An article with a very similar title was already submitted.']

    @patch("requests.get")
    @patch("requests.head")
    def test_9_post_ignore_article_with_almost_same_text(self, mock_head, mock_get, client):
        """
        testing when adding a new article.
        """
        self.clean_existing_elements()
        mock_get.return_value = MockResponse()
        mock_head.return_value = MockResponse()
        client.post(self._main_endpoint, data={'url': 'http://newsfromnyt.com'})

        # Edit Article to have almost same title
        article = ArticleModel.objects.get({"url": 'http://newsfromnyt.com'})
        article.title = 'My Completely different title.'
        article.text += ' - '
        article.save()

        # call the method `post`
        r = client.post(self._main_endpoint, data={'url': 'http://mydifferentcity.com'})
        data = json.loads(r.data)

        # Db query
        article_qs = ArticleModel.objects.raw({"url": 'http://mydifferentcity.com'})

        # Assert
        assert article_qs.count() == 0
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        assert data['Response']['errors'] == ['An article with a very similar text was already submitted.']
