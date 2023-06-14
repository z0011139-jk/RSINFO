from flask import Flask

from applications.view.bus.material import bus_material


def register_bus_views(app: Flask):
    app.register_blueprint(bus_material)
