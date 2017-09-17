import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, schema

from modelapp import config

db = SQLAlchemy()


def serialize(d, keys):
    return {c: getattr(d, c) for c in inspect(d).attrs.keys() if c in keys}


class Inputs(db.Model):
    __tablename__ = 'inputs_{}'.format(config.MODEL_VERSION)
    __table_args__ = (schema.UniqueConstraint('id', 'request_time', name='id_request_time_{}'.format(config.MODEL_VERSION)),)

    run_id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    id = db.Column(db.String, nullable=False)
    request_time = db.Column(db.DateTime, nullable=False)

    sepal_length = db.Column(db.Float(), nullable=True)
    sepal_width = db.Column(db.Float(), nullable=True)
    pental_length = db.Column(db.Float(), nullable=True)
    pental_width = db.Column(db.Float(), nullable=True)

    output = db.relationship('Outputs', backref='input', lazy='dynamic')

    def __repr__(self):
        return '<Inputs {}>'.format(self.run_id)


class Outputs(db.Model):
    __tablename__ = 'outputs_{}'.format(config.MODEL_VERSION)

    run_id = db.Column(db.Integer,
                       db.ForeignKey('inputs_{}.run_id'.format(config.MODEL_VERSION)),
                       primary_key=True)
    id = db.Column(db.String, nullable=False)
    finished_at = db.Column(db.DateTime, nullable=False)
    output = db.Column(db.String, nullable=False)
    code_version = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Outputs {}>'.format(self.run_id)
