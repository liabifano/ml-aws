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
                                   'scores': '/output/<id>/',
                                   'inputs': '/inputs/<id>/'},
                           'POST': {'score': '/run/'}}
        result = json.loads(self.client.get('/endpoints/').get_data(as_text=True))
        assert expected_result == result

    def test_output(self):
        output = Outputs(run_id=1,
                         id='1',
                         finished_at=datetime(2017, 1, 1),
                         output='1',
                         code_version='v')

        db.session.add(output)
        db.session.commit()
        expected_result = [{'id': '1',
                            'finished_at': 'Sun, 01 Jan 2017 00:00:00 GMT',
                            'output': '1',
                            'run_id': 1}]
        result = json.loads(self.client.get('/output/1/').get_data(as_text=True))
        assert expected_result == result

    def test_run(self):
        request = json.dumps(dict(id='1',
                                  request_time='2017-07-27 14:09:16.595260',
                                  inputs=dict(sepal_length=1.0,
                                              sepal_width=2.0,
                                              pental_length=3.0,
                                              pental_width=4.0)))
        result = self.client.post('/run/', data=request, content_type='application/json')
        assert result.status_code == 200
