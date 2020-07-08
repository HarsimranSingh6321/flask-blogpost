from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail , Message
from flask import Flask , Blueprint
from flask_bootstrap import Bootstrap
from flask_login import LoginManager 
from blogpost.config import Config

# app=Flask(__name__)
db=SQLAlchemy()
Bootstrap()
login_manager=LoginManager()
mail=Mail()




login_manager.login_view = 'users.login'  #similar as url_for function it will also lead to login function inside blueprint users
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
	app=Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	Bootstrap().init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)


	#Registerig Blueprints
	from blogpost.users.routes import users
	from blogpost.main.routes import main
	from blogpost.posts.routes import posts
	from blogpost.errors.handler import errors

	app.register_blueprint(users)
	app.register_blueprint(main)
	app.register_blueprint(posts)
	app.register_blueprint(errors)

	return app
