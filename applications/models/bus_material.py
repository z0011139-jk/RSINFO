import datetime
from applications.extensions import db


class Material(db.Model):
    __tablename__ = 'bus_material'
    id = db.Column(db.Integer, primary_key=True, comment='物料ID')
    materialNo = db.Column(db.String(255), comment='物料编号')
    materialName = db.Column(db.String(255), comment='物料名称')
    remark = db.Column(db.String(255), comment='备注')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')