from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# LoginManager.login_message = u"Bonvolu ensaluti por uzi tiunpaĝon"
# LoginManager.Login_message_category = 'info'

import views,models