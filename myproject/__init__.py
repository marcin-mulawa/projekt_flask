import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = r'\xc5\xba\xeb\xb6F\xaa\xdaDN\xc4\xe3\x80ez\xd1:?\xa9\x0c\x14\xf2\xd2\xa4j'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from myproject.files.views import files_blueprint

app.register_blueprint(files_blueprint,url_prefix="/files")
