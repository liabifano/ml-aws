import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, schema

db = SQLAlchemy()


def serialize(d, keys):
    return {c: getattr(d, c) for c in inspect(d).attrs.keys() if c in keys}


class Inputs(db.Model):
    version_model = open(os.path.join(os.path.abspath(os.path.join(__file__, "../../../..")), 'VERSION')).read()
    __tablename__ = 'inputs_{}'.format(version_model)
    __table_args__ = (schema.UniqueConstraint('client_id', 'request_time', name='client_id_request_time'),)

    run_id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    client_id = db.Column(db.String, nullable=False)
    request_time = db.Column(db.DateTime, nullable=False)

    a = db.Column(db.Integer(), nullable=True)
    b = db.Column(db.Integer(), nullable=True)

    output = db.relationship('Outputs', backref='input', lazy='dynamic')

    def __repr__(self):
        return '<Inputs {}>'.format(self.run_id)


class Outputs(db.Model):
    version_model = open(os.path.join(os.path.abspath(os.path.join(__file__, "../../../..")), 'VERSION')).read()
    __tablename__ = 'outputs_{}'.format(version_model)

    run_id = db.Column(db.Integer,
                       db.ForeignKey('inputs_{}.run_id'.format(version_model)),
                       primary_key=True)
    client_id = db.Column(db.String, nullable=False)
    finished_at = db.Column(db.DateTime, nullable=False)
    output = db.Column(db.Integer, nullable=False)
    code_version = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Outputs {}>'.format(self.run_id)
