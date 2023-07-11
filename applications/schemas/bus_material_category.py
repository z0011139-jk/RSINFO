from applications.extensions import ma
from marshmallow import fields, validate


class MaterialCategoryOutSchema(ma.Schema):
    id = fields.Integer()
    parent = fields.Integer()
    code = fields.Str(attribute="code")
    remark = fields.Str(attribute="remark")
    create_at = fields.DateTime()
    update_at = fields.DateTime()
