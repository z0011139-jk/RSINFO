import time

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from applications.common.curd import model_to_dicts, enable_status, disable_status, get_one_by_id
from applications.common.utils.http import table_api, success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Sell, SellDetail
from applications.schemas import SellOutSchema, SellDetailSchema

admin_sell = Blueprint('adminSell', __name__, url_prefix='/admin/sell')


# 销售单管理
@admin_sell.get('/')
@authorize("admin:sell:main")
def main():
    return render_template('admin/sell/main.html')


# 表格数据
@admin_sell.get('/data')
@authorize("admin:sell:main")
def table():
    sellOrderNo = str_escape(request.args.get('sellOrderNo', type=str))
    filters = []
    if sellOrderNo:
        filters.append(Sell.sellOrderNo.contains(sellOrderNo))
    sells = Sell.query.filter(*filters).layui_paginate()
    return table_api(data=model_to_dicts(schema=SellOutSchema, data=sells.items), count=sells.total)


# 销售单增加
@admin_sell.get('/add')
@authorize("admin:sell:add", log=True)
def add():
    return render_template('admin/sell/add.html')


# 销售单增加
@admin_sell.post('/save')
@authorize("admin:sell:add", log=True)
def save():
    req = request.get_json(force=True)
    date = time.strftime('%Y%m%d', time.localtime())
    sell = Sell.query.filter(Sell.sellOrderNo.like(date + '%')).order_by(Sell.sellOrderNo.desc()).first()
    sellOrderNo = ''
    if not sell:
        sellOrderNo = date + '0001'
    else:
        sellOrderNo = date + str(int(sell.sellOrderNo[8:]) + 1).rjust(4, "0")
    remark = str_escape(req.get("remark"))
    sell = Sell(
        sellOrderNo=sellOrderNo,
        remark=remark
    )
    db.session.add(sell)
    db.session.commit()
    return success_api(msg="成功")


# 销售单编辑
@admin_sell.get('/edit/<int:id>')
@authorize("admin:sell:edit", log=True)
def edit(id):
    s = get_one_by_id(model=Sell, id=id)
    return render_template('admin/sell/edit.html', sell=s)


# 更新销售单
@admin_sell.put('/update')
@authorize("admin:sell:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id = req_json.get("sellId")
    data = {
        "remark": str_escape(req_json.get("remark"))
    }
    sell = Sell.query.filter_by(id=id).update(data)
    db.session.commit()
    if not sell:
        return fail_api(msg="更新销售单失败")
    return success_api(msg="更新销售单成功")


# 销售单明细
@admin_sell.get('/detail/<int:id>')
@authorize("admin:sell:detail", log=True)
def detail(id):
    return render_template('admin/sell/detail.html', orderid=id)


# 销售单删除
@admin_sell.delete('/remove/<int:id>')
@authorize("admin:sell:remove", log=True)
def remove(id):
    s = Sell.query.filter_by(id=id).delete()
    db.session.commit()
    if not s:
        return fail_api(msg="销售单删除失败")
    return success_api(msg="销售单删除成功")


# 批量删除
@admin_sell.delete('/batchRemove')
@authorize("admin:sell:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    for id in ids:
        s = Sell.query.filter_by(id=id).delete()
    db.session.commit()
    return success_api(msg="批量删除成功")


######################################################  detail ########################################################

# 明细数据
@admin_sell.get('detail/data/<int:id>')
@authorize("admin:sell:detail")
def detailtable(id):
    selldetails = SellDetail.query.filter_by(sellOrderId=id).layui_paginate()
    return table_api(data=model_to_dicts(schema=SellDetailSchema, data=selldetails.items), count=selldetails.total)


# 销售单明细增加
@admin_sell.get('/detail/add/<int:id>')
@authorize("admin:sell:detail:add", log=True)
def adddetail(id):
    return render_template('admin/sell/adddetail.html', orderid=id)


# 销售单增加
@admin_sell.post('/detail/save')
@authorize("admin:sell:detail:add", log=True)
def savedetail():
    req = request.get_json(force=True)
    orderid = str_escape(req.get("orderid"))
    materialName = str_escape(req.get("materialName"))
    qty = str_escape(req.get("qty"))
    remark = str_escape(req.get("remark"))
    selldetail = SellDetail(
        sellOrderId=orderid,
        materialName=materialName,
        qty=qty,
        remark=remark
    )
    db.session.add(selldetail)
    db.session.commit()
    return success_api(msg="成功")

# 销售单明细编辑
@admin_sell.get('/detail/edit/<int:id>')
@authorize("admin:sell:detail:edit", log=True)
def editdetail(id):
    sd = get_one_by_id(model=SellDetail, id=id)
    return render_template('admin/sell/editdetail.html', selldetail=sd)

# 更新销售单明细
@admin_sell.put('/detail/update')
@authorize("admin:sell:detail:edit", log=True)
def updatedetail():
    req_json = request.get_json(force=True)
    id = req_json.get("id")
    data = {
        "materialNo": str_escape(req_json.get("materialNo")),
        "qty": str_escape(req_json.get("qty")),
        "remark": str_escape(req_json.get("remark"))
    }
    selldetail = SellDetail.query.filter_by(id=id).update(data)
    db.session.commit()
    if not selldetail:
        return fail_api(msg="更新销售单明细失败")
    return success_api(msg="更新销售单明细成功")

# 销售单明细删除
@admin_sell.delete('/detail/remove/<int:id>')
@authorize("admin:sell:detail:remove", log=True)
def removedetail(id):
    sd = SellDetail.query.filter_by(id=id).delete()
    db.session.commit()
    if not sd:
        return fail_api(msg="销售单明细删除失败")
    return success_api(msg="销售单明细删除成功")

# 批量删除
@admin_sell.delete('/detail/batchRemove')
@authorize("admin:sell:detail:remove", log=True)
def detailbatch_remove():
    ids = request.form.getlist('ids[]')
    for id in ids:
        sd = SellDetail.query.filter_by(id=id).delete()
    db.session.commit()
    return success_api(msg="批量删除成功")