from flask import Flask

from applications.view.bus.material import bus_material
from applications.view.bus.sell import bus_sell


def register_bus_views(app: Flask):
    app.register_blueprint(bus_material)
    app.register_blueprint(bus_sell)
    app.register_blueprint(bus_contact)
