import requests

from bs4 import BeautifulSoup


LIST_IGNORED_WORDS = ['that', 'this', 'those']


class ArticleParser(object):

    def __init__(self, url):
        self.response = requests.get(url)
        self.parsed_content = BeautifulSoup(self.response.content, 'html.parser')
        self.title = self.parsed_content.head.title.get_text()
        self.tags = None
        self.text = None

    def get_title(self):
        return self.title

    def get_tags(self):
        if self.tags is None:
            if self.text is None:
                self.get_text()

            words_dict = {}
            word_list = self.text.split()
            for word in word_list:
                word = word.strip()
                if len(word) < 4 or word in LIST_IGNORED_WORDS:
                    continue
                if word in words_dict:
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1

            self.tags = max(words_dict, key=words_dict.get)
        return self.tags

    def get_text(self):
        if self.text is None:
            self.text = ""
            for tag_p in self.parsed_content.find_all('p'):
                self.text += "\n" + tag_p.get_text()
        return self.text
