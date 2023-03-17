import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {'stores': list(stores.values())}


@app.post("/store")
def create_store():
    # get the request data
    store_data = request.get_json()

    store_id = uuid.uuid4().hex
    # create a variable to store the new store
    new_store = {**store_data, "id": store_id}
    # append the new store to the stores list
    stores[store_id] = new_store
    # return the new store
    return new_store, 201


@app.post("/item")
def create_item():
    # get the request data
    item_data = request.get_json()

    store_id = item_data.get('store_id', None)

    # If store_id is not provided or store_id is not in stores
    if not store_id or store_id not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    # create a variable to store the new item
    new_item = {**item_data, "id": item_id}
    # append the new item to the items list
    items[item_id] = new_item
    # return the new item
    return new_item, 201


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    store = stores.get(store_id, None)
    if store:
        return store
    abort(404, message="Store not found")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    item = items.get(item_id, None)
    if item:
        return item
    abort(404, message="Item not found")
