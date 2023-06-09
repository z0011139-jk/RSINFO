import datetime
from applications.extensions import db


class SellDetail(db.Model):
    __tablename__ = 'admin_selldetail'
    id = db.Column(db.Integer, primary_key=True, comment='销售单明细ID')
    sellOrderId = db.Column(db.Integer, comment='销售单Id')
    materialNo = db.Column(db.String(45), comment='物料编号')
    qty = db.Column(db.Integer, comment='物料数量')
    remark = db.Column(db.String(255), comment='备注')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')
