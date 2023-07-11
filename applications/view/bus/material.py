import time

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from applications.common import curd
from applications.common.curd import model_to_dicts, enable_status, disable_status, get_one_by_id
from applications.common.utils.http import table_api, success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Material, MaterialCategory
from applications.schemas import MaterialSchema

bus_material = Blueprint('busMaterial', __name__, url_prefix='/bus/material')


# 物料管理
@bus_material.get('/')
@authorize("bus:material:main")
def main():
    return render_template('bus/material/main.html')


# 表格数据
@bus_material.get('/data')
@authorize("bus:material:main")
def table():
    name = str_escape(request.args.get('name', type=str))
    materialcategoryid = request.args.get('materialcategoryid', type=int)
    filters = []
    if name:
        filters.append(Material.name.contains(name))
    if materialcategoryid:
        filters.append(Material.category == materialcategoryid)

    query = db.session.query(
        Material,
        MaterialCategory
    ).filter(*filters).outerjoin(MaterialCategory, Material.category == MaterialCategory.id).layui_paginate()
    return table_api(
        data=[{
            'id': material.id,
            'name': material.name,
            'detail': material.detail,
            'category': materialcategory.code if materialcategory else None,
            'barcode': material.barcode,
            'cost': material.cost,
            'price': material.price,
            'unit': material.unit,
            'threshold': material.threshold,
            'vendor': material.vendor,
            'manufacturer': material.manufacturer,
            'mpq': material.mpq,
            'moq': material.moq,
            'virtual': material.virtual,
            'highlight': material.highlight,
            'remark': material.remark,
            'create_time': material.create_time,
            'update_time': material.update_time
        } for material, materialcategory in query.items],
        count=query.total)


# 物料增加
@bus_material.get('/add')
@authorize("bus:material:add", log=True)
def add():
    return render_template('bus/material/add.html')


# 联系对象增加
@bus_material.post('/save')
@authorize("bus:material:add", log=True)
def save():
    req = request.get_json(force=True)
    name = str_escape(req.get("name"))
    detail = str_escape(req.get("detail")) if (str_escape(req.get("detail")) is not None) else ''
    category = str_escape(req.get("categoryid"))
    barcode = str_escape(req.get("barcode")) if (str_escape(req.get("barcode")) is not None) else ''
    cost = str_escape(req.get("cost")) if (str_escape(req.get("cost")) is not None) else ''
    price = str_escape(req.get("price")) if (str_escape(req.get("price")) is not None) else ''
    unit = str_escape(req.get("unit")) if (str_escape(req.get("unit")) is not None) else ''
    threshold = str_escape(req.get("threshold")) if (str_escape(req.get("threshold")) is not None) else ''
    vendor = str_escape(req.get("vendor")) if (str_escape(req.get("vendor")) is not None) else ''
    manufacturer = str_escape(req.get("manufacturer")) if (str_escape(req.get("manufacturer")) is not None) else ''
    mpq = str_escape(req.get("mpq")) if (str_escape(req.get("mpq")) is not None) else ''
    moq = str_escape(req.get("moq")) if (str_escape(req.get("moq")) is not None) else ''
    virtual = str_escape(req.get("virtual"))
    highlight = str_escape(req.get("highlight"))
    remark = str_escape(req.get("remark")) if (str_escape(req.get("remark")) is not None) else ''

    if not name:
        return fail_api(msg="物料名称不能为空！")

    material = Material(
        name=name,
        detail=detail,
        category=category,
        barcode=barcode,
        cost=cost,
        price=price,
        unit=unit,
        threshold=threshold,
        vendor=vendor,
        manufacturer=manufacturer,
        mpq=mpq,
        moq=moq,
        virtual=virtual,
        highlight=highlight,
        remark=remark
    )
    db.session.add(material)
    db.session.commit()
    return success_api(msg="添加成功")


# 删除物料
@bus_material.delete('/remove/<int:id>')
@authorize("bus:material:remove", log=True)
def delete(id):
    res = Material.query.filter_by(id=id).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


#  编辑物料
@bus_material.get('/edit/<int:id>')
@authorize("bus:material:edit", log=True)
def edit(id):
    material = curd.get_one_by_id(Material, id)
    return render_template('bus/material/edit.html', material=material)


#  编辑物料
@bus_material.put('/update')
@authorize("bus:material:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id = str_escape(req_json.get("id"))
    name = str_escape(req_json.get("name"))
    detail = str_escape(req_json.get("detail")) if (str_escape(req_json.get("detail")) is not None) else ''
    category = str_escape(req_json.get("categoryid")) if (str_escape(req_json.get("categoryid")) is not None) else ''
    barcode = str_escape(req_json.get("barcode")) if (str_escape(req_json.get("barcode")) is not None) else ''
    cost = str_escape(req_json.get("cost")) if (str_escape(req_json.get("cost")) is not None) else ''
    price = str_escape(req_json.get("price")) if (str_escape(req_json.get("price")) is not None) else ''
    unit = str_escape(req_json.get("unit")) if (str_escape(req_json.get("unit")) is not None) else ''
    threshold = str_escape(req_json.get("threshold")) if (str_escape(req_json.get("threshold")) is not None) else ''
    vendor = str_escape(req_json.get("vendor")) if (str_escape(req_json.get("vendor")) is not None) else ''
    manufacturer = str_escape(req_json.get("manufacturer")) if (str_escape(req_json.get("manufacturer")) is not None) else ''
    mpq = str_escape(req_json.get("mpq")) if (str_escape(req_json.get("mpq")) is not None) else ''
    moq = str_escape(req_json.get("moq")) if (str_escape(req_json.get("moq")) is not None) else ''
    virtual = str_escape(req_json.get("virtual"))
    highlight = str_escape(req_json.get("highlight"))
    remark = str_escape(req_json.get("remark")) if (str_escape(req_json.get("remark")) is not None) else ''

    Material.query.filter_by(id=id).update({
        'name': name,
        'detail': detail,
        'category': category,
        'barcode': barcode,
        'cost': cost,
        'price': price,
        'unit': unit,
        'threshold': threshold,
        'vendor': vendor,
        'manufacturer': manufacturer,
        'mpq': mpq,
        'moq': moq,
        'virtual': virtual,
        'highlight': highlight,
        'remark': remark
    })
    db.session.commit()
    return success_api(msg="更新成功")

# 批量删除
@bus_material.delete('/batchRemove')
@authorize("bus:material:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    for id in ids:
        res = Material.query.filter_by(id=id).delete()
    db.session.commit()
    return success_api(msg="批量删除成功")