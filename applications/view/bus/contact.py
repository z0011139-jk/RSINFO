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

bus_contact = Blueprint('busContact', __name__, url_prefix='/bus/contact')


# 联系对象管理
@bus_contact.get('/')
@authorize("bus:contact:main")
def main():
    return render_template('bus/contact/main.html')


# 表格数据
@bus_contact.get('/data')
@authorize("bus:contact:main")
def table():
    name = str_escape(request.args.get('name', type=str))
    filters = []
    if name:
        filters.append(Contact.name.contains(name))
    contacts = Contact.query.filter(*filters).layui_paginate()
    return table_api(data=model_to_dicts(schema=ContactSchema, data=contacts.items), count=contacts.total)


# 联系对象增加
@bus_contact.get('/add')
@authorize("bus:contact:add", log=True)
def add():
    return render_template('bus/contact/add.html')


# 联系对象增加
@bus_contact.post('/save')
@authorize("bus:contact:add", log=True)
def save():
    req = request.get_json(force=True)
    name = str_escape(req.get("name"))
    shortname = str_escape(req.get("shortname")) if (str_escape(req.get("shortname")) is not None) else ''
    address = str_escape(req.get("address")) if (str_escape(req.get("address")) is not None) else ''
    taxid = str_escape(req.get("taxid")) if (str_escape(req.get("taxid")) is not None) else ''
    contacter = str_escape(req.get("contacter")) if (str_escape(req.get("contacter")) is not None) else ''
    phone = str_escape(req.get("phone")) if (str_escape(req.get("phone")) is not None) else ''
    email = str_escape(req.get("email")) if (str_escape(req.get("email")) is not None) else ''
    website = str_escape(req.get("website")) if (str_escape(req.get("website")) is not None) else ''
    remark = str_escape(req.get("remark")) if (str_escape(req.get("remark")) is not None) else ''
    relation = str_escape(req.get("relation"))
    contact = Contact(
        name=name,
        shortname=shortname,
        address=address,
        taxid=taxid,
        contacter=contacter,
        phone=phone,
        email=email,
        website=website,
        remark=remark,
        relation=relation
    )
    db.session.add(contact)
    db.session.commit()
    return success_api(msg="成功")


# 联系对象编辑
@bus_contact.get('/edit/<int:id>')
@authorize("bus:contact:edit", log=True)
def edit(id):
    c = get_one_by_id(model=Contact, id=id)
    return render_template('bus/contact/edit.html', contact=c)


# 更新联系对象
@bus_contact.put('/update')
@authorize("bus:contact:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id = req_json.get("contactId")
    data = {
        "name": str_escape(req_json.get("name")),
        "shortname": str_escape(req_json.get("shortname")) if (str_escape(req_json.get("shortname")) is not None) else '',
        "address": str_escape(req_json.get("address")) if (str_escape(req_json.get("address")) is not None) else '',
        "taxid": str_escape(req_json.get("taxid")) if (str_escape(req_json.get("taxid")) is not None) else '',
        "contacter": str_escape(req_json.get("contacter")) if (str_escape(req_json.get("contacter")) is not None) else '',
        "phone": str_escape(req_json.get("phone")) if (str_escape(req_json.get("phone")) is not None) else '',
        "email": str_escape(req_json.get("email")) if (str_escape(req_json.get("email")) is not None) else '',
        "website": str_escape(req_json.get("website")) if (str_escape(req_json.get("website")) is not None) else '',
        "remark": str_escape(req_json.get("remark")) if (str_escape(req_json.get("remark")) is not None) else '',
        "relation": str_escape(req_json.get("relation"))
    }
    contact = Contact.query.filter_by(id=id).update(data)
    db.session.commit()
    if not contact:
        return fail_api(msg="更新联系人失败")
    return success_api(msg="更新联系人成功")


# 联系对象删除
@bus_contact.delete('/remove/<int:id>')
@authorize("bus:contact:remove", log=True)
def remove(id):
    c = Contact.query.filter_by(id=id).delete()
    db.session.commit()
    if not c:
        return fail_api(msg="联系人删除失败")
    return success_api(msg="联系人删除成功")


# 批量删除
@bus_contact.delete('/batchRemove')
@authorize("bus:contact:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    for id in ids:
        c = Contact.query.filter_by(id=id).delete()
    db.session.commit()
    return success_api(msg="批量删除成功")
