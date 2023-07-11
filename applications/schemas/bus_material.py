from applications.extensions import ma
from marshmallow import fields


class MaterialSchema(ma.Schema):
    id = fields.Integer()
    name = fields.Str(attribute="name")
    detail = fields.Str(attribute="detail")
    category = fields.Str(attribute="category")
    barcode = fields.Str(attribute="barcode")
    cost = fields.Str(attribute="cost")
    price = fields.Str(attribute="price")
    unit = fields.Str(attribute="unit")
    threshold = fields.Str(attribute="threshold")
    vendor = fields.Str(attribute="vendor")
    manufacturer = fields.Str(attribute="manufacturer")
    mpq = fields.Integer
    moq = fields.Integer
    virtual = fields.Integer
    highlight = fields.Integer
    remark = fields.Str(attribute="remark")
    create_at = fields.DateTime()
    update_at = fields.DateTime()
