import datetime
from applications.extensions import db


class Sell(db.Model):
    __tablename__ = 'bus_sell'
    id = db.Column(db.Integer, primary_key=True, comment='销售单ID')
    sellOrderNo = db.Column(db.String(255), comment='销售单编号')
    remark = db.Column(db.String(255), comment='备注')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')
