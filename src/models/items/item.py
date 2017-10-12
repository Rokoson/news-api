import uuid
import requests
from src.models.sites.site import SiteModel
from bs4 import BeautifulSoup
import re
import src.models.items.constants as itemConstants
from src.common.database import Database

__author__ = 'doolagunju'


class ItemModel(object):
    def __init__(self, source, pub_date=None, author=None, title=None, description=None,
                 content=None, url=None, char_count=None, word_count=None,_id=None):
        self.source = source
        self.pub_date = pub_date
        self.author = author
        self.title = title
        self.description = description
        self.content = content
        self.url = url
        self.char_count = char_count
        self.word_count = word_count
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def get_links(url_prefix, story_link):
        links = []
        request = requests.get(url_prefix)
        bsObj = BeautifulSoup(request.content, 'html.parser')
        tag = story_link['tag_name']
        key, value = story_link['query']
        stories = bsObj.findAll(tag, {key: value})
        for story in stories:
            link = story.find("a")
            if link is not None and link.attrs['href'][1:8] == 'article':
                print(link.attrs['href'])
                links.append(url_prefix + link.attrs['href'])
        return links

    @staticmethod
    def parse_html(soup, tag_params):
        tag = tag_params['tag_name']
        key, value = tag_params['query']
        attr = tag_params['attr']
        #print("tag: {} key: {} value: {} attr: {}".format(tag, key, value, attr))
        parsed_item = soup.find(tag, {key:value})
        return soup.find(tag, {key: value}).attrs[attr]

    def get_article(self, article_url, site):
        self.url = article_url
        request = requests.get(article_url)
        soup = BeautifulSoup(request.content, 'html.parser')

        author_tag = site.author_tag
        self.author = self.parse_html(soup,author_tag)

        date_tag = site.date_tag
        self.pub_date = self.parse_html(soup, date_tag)

        content_tag = site.content_tag
        content = soup.find(content_tag['tag_name'],
                            {content_tag['query'][0]: re.compile("^" + content_tag['query'][1])}).findAll('p')
        content =[par.text for par in content]
        self.content = content

        self.char_count = sum([len(p) for p in content])
        self.word_count = sum([len(p.split(' ')) for p in content])

        title_tag = site.title_tag
        self.title = self.parse_html(soup, title_tag)

        description_tag = site.description_tag
        self.description = self.parse_html(soup, description_tag)

        Database.insert(itemConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "source": self.source,
            "pub_date": self.pub_date,
            "author": self.author,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "url": self.url,
            "word_count": self.word_count,
            "char_count": self.char_count
        }

    @classmethod
    def get_by_query(cls, search_query):
        results = Database.find_by_text(itemConstants.COLLECTION, search_query)
        return [cls(**{k: v for (k, v) in elem.items() if k != 'score' and v is not None}) for elem in results]

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(itemConstants.COLLECTION, {'_id': item_id}))
