import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Stores related operations")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = stores.get(store_id, None)
        if store:
            return store
        abort(404, message="Store not found")

    def delete(self, store_id):
        store = stores.get(store_id, None)
        if store:
            del stores[store_id]
            return {"message": "Store deleted"}
        abort(404, message="Store not found")

@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        # get the request data

        # If same store already exists, abort
        for store in stores.values():
            if store['name'] == store_data['name']:
                abort(400, message="Store already exists")

        store_id = uuid.uuid4().hex
        # create a variable to store the new store
        new_store = {**store_data, "id": store_id}
        # append the new store to the stores list
        stores[store_id] = new_store
        # return the new store
        return new_store