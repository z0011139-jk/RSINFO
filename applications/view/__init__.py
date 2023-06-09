from applications.view.admin import register_admin_views
from applications.view.bus import register_bus_views
from applications.view.index import register_index_views
from applications.view.passport import register_passport_views
from applications.view.rights import register_rights_view
from applications.view.department import register_dept_views
from applications.view.plugin import register_plugin_views

def init_view(app):
    register_admin_views(app)
    register_bus_views(app)
    register_index_views(app)
    register_rights_view(app)
    register_passport_views(app)
    register_dept_views(app)
    register_plugin_views(app)
