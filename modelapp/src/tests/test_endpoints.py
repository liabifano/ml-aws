import json
import unittest
from datetime import datetime

from modelapp.db_models import db, Outputs
from . import app


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        db.init_app(app)
        db.app = app
        db.create_all()

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        result = self.client.get('/')
        assert result.status_code == 200

    def test_version(self):
        result = self.client.get('/version/')
        assert result.status_code == 200

    def test_endpoints(self):
        expected_result = {'GET': {'version': '/version/',
                                   'scores': '/output/<client-id>/',
                                   'inputs': '/inputs/<client-id>/'},
                           'POST': {'score': '/run/'}}
        result = json.loads(self.client.get('/endpoints/').get_data(as_text=True))
        assert expected_result == result

    def test_output(self):
        output = Outputs(run_id=1,
                         client_id='1',
                         finished_at=datetime(2017, 1, 1),
                         output=3,
                         code_version='v')

        db.session.add(output)
        db.session.commit()
        expected_result = [{'client_id': '1',
                            'finished_at': 'Sun, 01 Jan 2017 00:00:00 GMT',
                            'output': 3,
                            'run_id': 1}]
        result = json.loads(self.client.get('/output/1/').get_data(as_text=True))
        assert expected_result == result

    def test_run(self):
        request = json.dumps(dict(client_id='1',
                                  request_time='2017-07-27 14:09:16.595260',
                                  inputs=dict(a=1, b=2)))
        result = self.client.post('/run/', data=request, content_type='application/json')
        assert result.status_code == 200
