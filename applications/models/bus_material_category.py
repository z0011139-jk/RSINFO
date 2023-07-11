import datetime
from applications.extensions import db


class MaterialCategory(db.Model):
    __tablename__ = 'bus_material_category'
    id = db.Column(db.Integer, primary_key=True, comment="物料分类ID")
    parent = db.Column(db.Integer, comment="父级编号")
    code = db.Column(db.String(255), comment="物料分类代码")
    remark = db.Column(db.String(255), comment="备注")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')