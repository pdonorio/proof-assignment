# -*- coding: utf-8 -*-

from restapi.models.sqlalchemy import db


class Examples(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(36), unique=True)
    truth = db.Column(db.Boolean)
    description = db.Column(db.Text())
    created = db.Column(db.DateTime)
    value = db.Column(db.Integer, default=1)
