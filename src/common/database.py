import pymongo
import os
import src.config

__author__ = 'omoekan'


class Database(object):

    # URI = "mongodb://127.0.0.1:27017"
    URI = os.environ.get('dgOcean_URI')
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        # Database.DATABASE = client.get_default_database()
        Database.DATABASE = client['news-scrapings']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_by_text(collection, text_query):
        return Database.DATABASE[collection].find({"$text": {"$search": text_query}},
                                                  {"score": {"$meta": "textScore"}}).sort([("textScore", pymongo.DESCENDING)])

    @staticmethod
    def find_top_n(collection, text_query, n=5):
        return Database.DATABASE[collection].find({"$text": {"$search": text_query}},
                                                  {"score": {"$meta": "textScore"}}).sort([("textScore", pymongo.DESCENDING)]).limit(n)
