from applications.extensions import ma
from marshmallow import fields


class SellDetailSchema(ma.Schema):
    id = fields.Integer()
    sellOrderId = fields.Integer()
    materialNo = fields.Str(attribute="materialNo")
    qty = fields.Integer()
    remark = fields.Str(attribute="remark")
    create_at = fields.DateTime()
    update_at = fields.DateTime()
