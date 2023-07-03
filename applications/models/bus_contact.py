import datetime
from applications.extensions import db


class Contact(db.Model):
    __tablename__ = 'bus_contact'
    id = db.Column(db.Integer, primary_key=True, comment='联系对象id')
    name = db.Column(db.String(255), comment='联系对象名称')
    shortname = db.Column(db.String(255), comment='别名')
    address = db.Column(db.String(255), comment='地址')
    taxid = db.Column(db.String(255), comment='税号')
    contacter = db.Column(db.String(255), comment='联系人')
    phone = db.Column(db.String(255), comment='电话')
    email = db.Column(db.String(255), comment='邮箱')
    website = db.Column(db.String(255), comment='网站')
    remark = db.Column(db.String(255), comment='备注')
    relation = db.Column(db.String(255), comment='关系')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')
