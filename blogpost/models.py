from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager ,UserMixin ,current_user
from datetime import  datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from blogpost import db

class User(UserMixin,db.Model):
    id=db.Column(db.Integer , primary_key=True)
    username=db.Column(db.String(20) , unique=True)
    email=db.Column(db.String(50), unique=True)
    password=db.Column(db.String(80))
    posts=db.relationship('Post' , backref='author' , lazy=True)

    def __repr__(self):
        return f"{self.username} , {self.email} , {self.password}"

    def get_reset_token(self , expire_sec = 1800):   #i.e 1800 seconds
        s = Serializer(current_app.config['SECRET_KEY'] , expire_sec)
        return s.dumps({'user_id' : self.id}).decode('utf-8')

    
    @staticmethod       # doesn't require self
    def verify_reset_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        
        return User.query.get(user_id)


class Post(UserMixin,db.Model):
    id=db.Column(db.Integer , primary_key=True)
    title=db.Column(db.String , nullable=False)
    content=db.Column(db.String , nullable=False)
    date_posted=db.Column(db.DateTime , nullable=False , default =datetime.utcnow())
    post_id=db.Column(db.Integer , db.ForeignKey('user.id'), nullable=False)