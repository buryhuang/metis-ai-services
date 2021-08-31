#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from apis import api

if __name__ == "__main__":
    app = Flask(__name__)
    api.init_app(app)

    app.run(debug=True)
