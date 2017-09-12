import unittest
from datetime import datetime

from modelapp.db_models import db, Inputs, Outputs
from . import app


class TestModels(unittest.TestCase):
    def setUp(self):
        db.init_app(app)
        db.app = app
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_inputs(self):
        input = Inputs(id='1',
                       request_time=datetime(2017, 1, 1),
                       sepal_length=1.0,
                       sepal_width=2.0,
                       pental_length=3.0,
                       pental_width=4.0)

        db.session.add(input)
        db.session.commit()

        queried = Inputs.query.filter_by(id='1').one()
        assert queried is not None

    def test_outputs(self):
        output = Outputs(run_id=1,
                         id='1',
                         finished_at=datetime(2017, 1, 1),
                         output=3,
                         code_version='v')

        db.session.add(output)
        db.session.commit()

        queried = Outputs.query.filter_by(id='1').one()
        assert queried is not None
