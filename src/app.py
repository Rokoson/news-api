from src.common.database import Database
from src.models.sites.site import SiteModel
from src.models.items.item import ItemModel
import pymongo
from src.models.items import constants as ItemConstants
from src.resources.item import Item, ItemList


__author__ = 'doolagunju'

from flask import Flask
from flask_restful import Api

app = Flask(__name__)  # '__main__'
app.config['DEBUG'] = True
app.secret_key = "lanre"
api = Api(app)

api.add_resource(ItemList, '/items/<string:query>')
api.add_resource(Item, '/item/<_id>')

if __name__ == '__main__':
    from src.common.database import Database

    @app.before_first_request
    def initialize_database():
        Database.initialize()


    app.run(port=5000)
