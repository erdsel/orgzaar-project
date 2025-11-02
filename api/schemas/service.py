from marshmallow import Schema, fields


class ServiceSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    price = fields.Int(required=True)
