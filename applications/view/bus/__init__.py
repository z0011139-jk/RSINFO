from flask import Flask

from applications.view.bus.materialcategory import bus_materialcategory
from applications.view.bus.material import bus_material
from applications.view.bus.sell import bus_sell
from applications.view.bus.contact import bus_contact


def register_bus_views(app: Flask):
    app.register_blueprint(bus_materialcategory)
    app.register_blueprint(bus_material)
    app.register_blueprint(bus_sell)
    app.register_blueprint(bus_contact)
