from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask import redirect

import stripe

SECRET_KEY = '********************'
PUB_KEY = '***********************'
stripe.api_key = SECRET_KEY

app = Flask(__name__)
mail = Mail(app)
app.config['SECRET_KEY'] = '***************'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

app.config['SECURITY_PASSWORD_SALT'] = '*****************'
app.config['RECAPTCHA_PUBLIC_KEY'] = '***************'
app.config['RECAPTCHA_PRIVATE_KEY'] = '*****************'

app.config.update(
    DEBUG = True,
    # Flask-Mail Configuration
    MAIL_SERVER = '***************',
    MAIL_USERNAME = '************',
    MAIL_PASSWORD = '***********',
    DEFAULT_MAIL_SENDER = '***************'
    )

db.create_all()
mail = Mail(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)