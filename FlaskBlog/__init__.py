import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from FlaskBlog.config import Config
#from flask_migrate import Migrate, MigrateCommand
#from flask_script import Manager




db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
from FlaskBlog.Model_s import *

def create_app(config_class=Config):
    application = Flask ( __name__ )
    application.config.from_object(config_class)
    db.init_app(application)
    bcrypt.init_app(application)
    login_manager.init_app(application)
    mail.init_app(application)
    # admin##
    admin = Admin(application)
    admin.add_view(ModelView( Post, db.session))
    admin.add_view(ModelView( Tag, db.session))
    admin.add_view(ModelView( Rpa, db.session))
    admin.add_view ( ModelView ( User, db.session ) )


    from FlaskBlog.users.Routes import users
    from FlaskBlog.posts.Routes import posts
    from FlaskBlog.main.Routes import main
    from FlaskBlog.RPA.Routes import rpa
    from FlaskBlog.errors.handlers import errors
    application.register_blueprint(users)
    application.register_blueprint(posts)
    application.register_blueprint(main)
    application.register_blueprint(errors)
    application.register_blueprint(rpa)
    return application



