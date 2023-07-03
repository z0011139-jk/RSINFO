import time

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from applications.common.curd import model_to_dicts, enable_status, disable_status, get_one_by_id
from applications.common.utils.http import table_api, success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Contact
from applications.schemas import ContactSchema

bus_contact = Blueprint('busContact', __name__, url_prefix='/bus/sell')


# 联系对象管理
@bus_contact.get('/')
@authorize("admin:contact:main")
def main():
    return render_template('bus/contact/main.html')


# 表格数据
@bus_contact.get('/data')
@authorize("admin:contact:main")
def table():
    name = str_escape(request.args.get('name', type=str))
    filters = []
    if name:
        filters.append(Contact.name.contains(name))
    contacts = Contact.query.filter(*filters).layui_paginate()
    return table_api(data=model_to_dicts(schema=ContactSchema, data=contacts.items), count=contacts.total)


# 联系对象增加
@bus_contact.get('/add')
@authorize("admin:contact:add", log=True)
def add():
    return render_template('bus/contact/add.html')


# 联系对象增加
@bus_contact.post('/save')
@authorize("admin:contact:add", log=True)
def save():
    req = request.get_json(force=True)
    name = str_escape(req.get("name"))
    shortname = str_escape(req.get("shortname"))
    address = str_escape(req.get("address"))
    
    remark = str_escape(req.get("remark"))
    contact = Contact(
        name=name,
        remark=remark
    )
    db.session.add(contact)
    db.session.commit()
    return success_api(msg="成功")


# 联系对象编辑
@bus_contact.get('/edit/<int:id>')
@authorize("admin:sell:edit", log=True)
def edit(id):
    s = get_one_by_id(model=Sell, id=id)
    return render_template('bus/sell/edit.html', sell=s)


# 更新联系对象
@bus_contact.put('/update')
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

# 联系对象删除
@bus_contact.delete('/remove/<int:id>')
@authorize("admin:sell:remove", log=True)
def remove(id):
    s = Sell.query.filter_by(id=id).delete()
    db.session.commit()
    if not s:
        return fail_api(msg="销售单删除失败")
    return success_api(msg="销售单删除成功")


# 批量删除
@bus_contact.delete('/batchRemove')
@authorize("admin:sell:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    for id in ids:
        s = Sell.query.filter_by(id=id).delete()
    db.session.commit()
    return success_api(msg="批量删除成功")
