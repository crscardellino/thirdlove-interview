# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Hello, World!"})

