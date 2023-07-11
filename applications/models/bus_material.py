import datetime
from applications.extensions import db


class Material(db.Model):
    __tablename__ = 'bus_material'
    id = db.Column(db.Integer, primary_key=True, comment='物料ID')
    name = db.Column(db.String(255), comment='物料名称')
    detail = db.Column(db.String(255), comment='物料说明')
    category = db.Column(db.Integer, comment='分类')
    barcode = db.Column(db.String(255), comment='条码')
    cost = db.Column(db.String(255), comment='成本')
    price = db.Column(db.String(255), comment='价格')
    unit = db.Column(db.String(255), comment='单位')
    threshold = db.Column(db.String(255), comment='提醒门限')
    vendor = db.Column(db.String(255), comment='供应商')
    manufacturer = db.Column(db.String(255), comment='制造商')
    mpq = db.Column(db.Integer, comment='最小包装数量')
    moq = db.Column(db.Integer, comment='最小起订量')
    virtual = db.Column(db.Integer, comment='虚拟物料')
    highlight = db.Column(db.Integer, comment='重点关注')
    remark = db.Column(db.String(255), comment='备注')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')