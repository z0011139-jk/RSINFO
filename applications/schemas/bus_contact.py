from applications.extensions import ma
from marshmallow import fields


class ContactSchema(ma.Schema):
    id = fields.Integer()
    name = fields.Str(attribute="name")
    shortname = fields.Str(attribute="shortname")
    address = fields.Str(attribute="address")
    taxid = fields.Str(attribute="taxid")
    contacter = fields.Str(attribute="contacter")
    phone = fields.Str(attribute="phone")
    email = fields.Str(attribute="email")
    website = fields.Str(attribute="website")
    remark = fields.Str(attribute="remark")
    relation = fields.Str(attribute="relation")
    create_at = fields.DateTime()
    update_at = fields.DateTime()
