from flask import Flask

from modelapp.endpoints import mod

app = Flask(__name__)
app.config.from_object('modelapp.config.TestConfig')
app.register_blueprint(mod)
