import re
import socket
from collections import Counter
from urllib.parse import urlparse
from urllib.request import urlopen

from articleDateExtractor import extractArticlePublishedDate
from bs4 import BeautifulSoup
from geolite2 import geolite2
from textblob import TextBlob


def parse_authors(authors):
    return [author.text.strip().title() for author in authors]


def extract_tags_from_article(article_text):
    keywords = TextBlob(article_text).noun_phrases
    counter = Counter(keywords)
    return counter.most_common(5)


def get_domain_data_from_url(url):
    domain = urlparse(url).netloc
    ip = socket.gethostbyname(domain)
    ip_reader = geolite2.reader()
    ip_data = ip_reader.get(ip)
    return domain, ip_data.get('registered_country', {}).get('iso_code')


def parse_article(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    for script in soup.find_all('script'):
        script.decompose()

    for style in soup.find_all('style'):
        style.decompose()

    article_data = {
        'url': url,
        'text': soup.body.text.strip().replace('\n', ' '),
    }

    source, country_code = get_domain_data_from_url(url)
    if source:
        article_data['source'] = source

    if country_code:
        article_data['country_code'] = country_code

    title = soup.find('title')
    if title:
        article_data['title'] = title.text.strip()

    authors = parse_authors(soup.find_all(attrs=re.compile('author')))
    if authors:
        article_data['authors'] = authors

    published_date = extractArticlePublishedDate(url, html=page)
    if published_date:
        article_data['published_date'] = published_date

    tags = extract_tags_from_article(soup.body.text.strip())
    if tags:
        article_data['tags'] = tags

    return article_data
