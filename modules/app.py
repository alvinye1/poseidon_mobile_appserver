# -*-coding: utf-8 -*-
"""
Created by jojo at 2018/9/7
Modified by Alvin at 2019/2/20 v2.0
"""

from flask import Flask
import modules.configs as configs
from controllers import blueprints

__all__ = ['create_app']


def create_app(app_name, config=None):
    app = Flask(app_name)
    configure_app(app, config)
    return app


def configure_app(app, config):
    app.config.from_object(configs.BaseConfig())
    if not config:
        config = configs.config_map['dev']
    app.config.from_object(config)
    # register blueprints
    for bp in blueprints:
        app.register_blueprint(bp)
