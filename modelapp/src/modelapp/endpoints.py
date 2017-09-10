import os
import pandas as pd

from flask import request, Blueprint
from flask_api import status
from flask_jsontools import jsonapi
import pkg_resources
from datetime import datetime

from modelapp.db_models import db, serialize, Inputs, Outputs
from modelapp import model, adapters

mod = Blueprint('endpoints', __name__)

@mod.route('/', methods=['GET'])
@jsonapi
def home():
    return status.HTTP_200_OK


@mod.route('/version/', methods=['GET'])
@jsonapi
def version():
    version_model = open(os.path.join(os.path.abspath(os.path.join(__file__, "../../../..")), 'VERSION')).read()
    version_code = pkg_resources.require('modelapp')[0].version
    return '{}-{}'.format(version_model, version_code)


@mod.route('/endpoints/', methods=['GET'])
@jsonapi
def endpoints():
    return {'GET': {'version': '/version/',
                    'scores': '/output/<client-id>/',
                    'inputs': '/inputs/<client-id>/'},
            'POST': {'score': '/run/'}}


@mod.route('/output/<string:client_id>/', methods=['GET'])
@jsonapi
def output(client_id):
    keys_to_show = ['run_id', 'client_id', 'finished_at', 'output', 'version']
    outputs = Outputs.query.filter(Outputs.client_id == client_id).all()

    return [serialize(o, keys_to_show) for o in outputs]


@mod.route('/run/', methods=['POST'])
@jsonapi
def run():
    request_json = request.json

    try:
        df = adapters.json_to_df(request_json)
        score = model.predict(df)
    except:
        RuntimeError('Not able to score to {}'.format(request_json['client_id']))

    inputs = Inputs(**df.to_dict('records')[0])
    outputs = Outputs(client_id=request_json['client_id'],
                      finished_at=datetime.utcnow(),
                      output=score,
                      code_version=pkg_resources.require('modelapp')[0].version)


    inputs.output.append(outputs)
    db.session.add_all([inputs])
    db.session.commit()

    return status.HTTP_201_CREATED
