import time

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from applications.common.curd import model_to_dicts, enable_status, disable_status, get_one_by_id
from applications.common.utils.http import table_api, success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Material
from applications.schemas import MaterialSchema

bus_material = Blueprint('busMaterial', __name__, url_prefix='/bus/material')


# 表格数据
@bus_material.get('/data')
def table():
    queryStr = str_escape(request.args.get('queryStr', type=str))
    filters = []
    if queryStr:
        filters.append(Material.materialName.contains(queryStr))
    materials = Material.query.filter(*filters).layui_paginate()
    return table_api(data=model_to_dicts(schema=MaterialSchema, data=materials.items), count=10)
