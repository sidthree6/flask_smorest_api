import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Items related operations")

@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = items.get(item_id, None)
        if item:
            return item
        abort(404, message="Item not found")

    def delete(self, item_id):
        item = items.get(item_id, None)
        if item:
            del items[item_id]
            return {"message": "Item deleted"}
        abort(404, message="Item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):

        item = items.get(item_id, None)
        if items:
            item |= item_data
            return item
        abort(404, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # get the request data

        store_id = item_data.get('store_id', None)

        # If store_id is not provided or store_id is not in stores
        if not store_id or store_id not in stores:
            abort(404, message="Store not found")

        # If same item in same store already exists, abort
        for item in items.values():
            if item['name'] == item_data['name'] and item['store_id'] == store_id:
                abort(400, message="Item already exists in this store")

        item_id = uuid.uuid4().hex
        # create a variable to store the new item
        new_item = {**item_data, "id": item_id}
        # append the new item to the items list
        items[item_id] = new_item
        # return the new item
        return new_item