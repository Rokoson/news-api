import uuid
from src.common.database import Database
import src.models.sites.constants as siteConstants

__author__ = 'doolagunju'

class SiteModel(object):
    def __init__(self, source, url_prefix, story_link, date_tag, author_tag,
                 title_tag, description_tag, content_tag, _id=None):
        self.source = source
        self.url_prefix = url_prefix
        self.story_link = story_link # dict- tag_name, query
        self.date_tag = date_tag # dict - with tag_name, query
        self.author_tag = author_tag
        self.title_tag = title_tag # dict
        self.description_tag = description_tag # dict
        self.content_tag = content_tag # dict
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Site {}>".format(self.source)

    def json(self):
        return {
            "_id": self._id,
            "source": self.source,
            "url_prefix": self.url_prefix,
            "story_link": self.story_link,
            "date_tag": self.date_tag,
            "author_tag": self.author_tag,
            "title_tag": self.title_tag,
            "description_tag": self.description_tag,
            "content_tag": self.content_tag
        }

    def save_to_mongo(self):
        Database.insert(siteConstants.COLLECTION, self.json())

    @classmethod
    def get_by_name(cls, site_name):
        return cls(**Database.find_one(siteConstants.COLLECTION, {"source": site_name}))