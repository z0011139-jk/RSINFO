from flask import Blueprint, render_template, request, jsonify

from applications.common import curd
from applications.common.utils import validate
from applications.common.utils.http import success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Material, MaterialCategory
from applications.schemas import MaterialCategoryOutSchema

bus_materialcategory = Blueprint('busMaterialCategory', __name__, url_prefix='/bus/materialcategory')


@bus_materialcategory.get('/')
@authorize("bus:materialcategory:main", log=True)
def main():
    return render_template('bus/materialcategory/main.html')


@bus_materialcategory.post('/data')
@authorize("bus:materialcategory:main", log=True)
def data():
    mc = MaterialCategory.query.order_by(MaterialCategory.code).all()
    data = curd.model_to_dicts(schema=MaterialCategoryOutSchema, data=mc)
    res = {
        "data": data
    }
    return jsonify(res)


@bus_materialcategory.get('/add')
@authorize("bus:materialcategory:add", log=True)
def add():
    return render_template('bus/materialcategory/add.html')


@bus_materialcategory.get('/tree')
@authorize("bus:materialcategory:main", log=True)
def tree():
    mc = MaterialCategory.query.order_by(MaterialCategory.code).all()
    data = curd.model_to_dicts(schema=MaterialCategoryOutSchema, data=mc)
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": data

    }
    return jsonify(res)


@bus_materialcategory.post('/save')
@authorize("bus:materialcategory:add", log=True)
def save():
    req = request.get_json(force=True)
    mc = MaterialCategory(
        parent=req.get('parent'),
        code=str_escape(req.get('code')),
        remark=str_escape(req.get("remark")) if (str_escape(req.get("remark")) is not None) else ''
    )
    db.session.add(mc)
    db.session.commit()
    return success_api(msg="成功")


@bus_materialcategory.get('/edit')
@authorize("bus:materialcategory:edit", log=True)
def edit():
    _id = request.args.get("id")
    mc = curd.get_one_by_id(model=MaterialCategory, id=_id)
    return render_template('bus/materialcategory/edit.html', materialcategory=mc)


@bus_materialcategory.put('/update')
@authorize("bus:materialcategory:edit", log=True)
def update():
    json = request.get_json(force=True)
    id = json.get("id"),
    data = {
        "code": validate.str_escape(json.get("code")),
        "remark": validate.str_escape(json.get("remark"))
    }
    d = MaterialCategory.query.filter_by(id=id).update(data)
    if not d:
        return fail_api(msg="更新失败")
    db.session.commit()
    return success_api(msg="更新成功")


@bus_materialcategory.delete('/remove/<int:_id>')
@authorize("bus:materialcategory:remove", log=True)
def remove(_id):
    d = MaterialCategory.query.filter_by(id=_id).delete()
    if not d:
        return fail_api(msg="删除失败")
    ms = Material.query.filter_by(category=_id).all()
    if ms:
        for m in ms:
            m.category = None
    db.session.commit()
    return success_api(msg="删除成功")
