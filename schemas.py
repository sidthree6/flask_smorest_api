from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
    store_id = fields.String(required=True)


class ItemUpdateSchema(Schema):
    name = fields.String()
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)