from flask_restful import Resource, reqparse
from src.models.items.item import ItemModel


class Item(Resource):
    def get(self, _id):
        item = ItemModel.get_by_id(_id)
        return item.json()


class ItemList(Resource):
    keys_to_display = ['_id', 'source', 'pub_date', 'author', 'title', 'description',
                       'word_count','char_count']

    def get(self, query):
        results = ItemModel.get_by_query(query)
        results = [x.json() for x in results]
        return {"items": [{k: d[k] for k in d.keys() if k in ItemList.keys_to_display}
                          for d in results]}
