from flask import Flask

from modelapp.db_models import db
from modelapp.endpoints import mod

app = Flask(__name__)
app.config.from_object('modelapp.config.DevConfig')
app.register_blueprint(mod)

db.init_app(app)
bootstrap = True
if bootstrap:
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run()
