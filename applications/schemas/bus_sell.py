from applications.extensions import ma
from marshmallow import fields


class SellOutSchema(ma.Schema):
    id = fields.Integer()
    sellOrderNo = fields.Str(attribute="sellOrderNo")
    remark = fields.Str(attribute="remark")
    create_at = fields.DateTime()
    update_at = fields.DateTime()
