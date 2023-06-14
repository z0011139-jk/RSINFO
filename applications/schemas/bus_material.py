from applications.extensions import ma
from marshmallow import fields


class MaterialSchema(ma.Schema):
    id = fields.Integer()
    MaterialNo = fields.Str(attribute="materialNo")
    MaterialName = fields.Str(attribute="materialName")
    remark = fields.Str(attribute="remark")
    create_at = fields.DateTime()
    update_at = fields.DateTime()
