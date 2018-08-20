import json
from unittest import TestCase

import requests


class Tester(TestCase):
    def setUp(self):
        self.host = 'http://localhost:8080/api/articles'

    def test_simple_post_get(self):
        url = 'https://www.newyorker.com/magazine/2018/08/27/gospels-of-giving-for-the-new-gilded-age'
        r = requests.post(self.host, data={'url': url})
        assert r.status_code == 200
        assert r.reason == 'OK'
        assert 'Success' in r.text

        r = requests.get(self.host, data={'url': url})
        assert json.loads(r.text)['Meta']['elements'] == 1
        assert json.loads(r.text)['Meta']['errors'] == 0
        assert (json.loads(json.loads(r.text)['Response']['data'])['_id']) == url

    def test_add_with_same_url(self):
        url = 'https://edition.cnn.com/2018/08/20/asia/korea-family-reunion-intl/index.html'
        r = requests.post(self.host, data={'url': url})
        assert r.status_code == 200
        assert r.reason == 'OK'
        assert 'Success' in r.text

        r = requests.post(self.host, data={'url': url})
        assert r.status_code == 500
        assert r.reason == 'INTERNAL SERVER ERROR'
        assert 'already exists' in r.text

    def test_add_article_with_similar_title(self):
        url_a = 'http://www.foxnews.com/politics/2018/08/19/ex-cia-director-brennans-anti-trump-comments-did-damage-to-intel-community-mullen-says.html'
        url_b = 'https://1010wcsi.com/fox-politics/ex-cia-director-brennans-anti-trump-comments-did-damage-to-intel-community-mullen-says/'
        r = requests.post(self.host, data={'url': url_a})
        assert r.status_code == 200
        assert r.reason == 'OK'
        assert 'Success' in r.text

        r = requests.post(self.host, data={'url': url_b})
        assert r.status_code == 500
        assert r.reason == 'INTERNAL SERVER ERROR'
        assert 'already been posted' in r.text

    def test_add_article_with_similar_content(self):
        # Shouldn't be this hard to find two articles with 80% same content. They hide only if you look for them.
        pass

    def test_get_all(self):
        r = requests.get(self.host)
        assert len(json.loads(json.loads(r.text)['Response']['data'])) > 1
        pass
