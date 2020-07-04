import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = r'6rf\bsdujhsudu<>Ig<()7gh1s/9dsfhk!jas8&9r413jhaduyzvcx\s'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')

DATASETS_DIRECTORY = 'myproject/datasets/saved'

db = SQLAlchemy(app)


from myproject.datasets.views import datasets_blueprint

app.register_blueprint(datasets_blueprint,url_prefix="/datasets")
