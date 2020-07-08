from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , BooleanField , SubmitField, ValidationError , TextAreaField
from wtforms.validators import InputRequired , Length , email , EqualTo 
from wtforms.validators import Email 
from blogpost.models import Post, User
from blogpost import Bootstrap , login_manager 
from flask_login import current_user




class LoginForm(FlaskForm):
    username=StringField('Username' , validators=[InputRequired(), Length(min=4 , max=20)])
    password=PasswordField('Password' , validators=[InputRequired() , Length(min=8 , max=80)])
    remember=BooleanField('remember me')
    submit=SubmitField('Login')

class RegisterForm(FlaskForm):
    email=StringField('Email' , validators=[InputRequired(), Email(message='Invalid Input') ,Length(max=50)])
    username=StringField('Username' , validators=[InputRequired(), Length(min=4 , max=20)])
    password=PasswordField('Password' , validators=[InputRequired() , Length(min=8 , max=80)])
    confirm_password=PasswordField('Confirm Password' , validators=[InputRequired() , EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data.lower()).first()
        if user:
            raise ValidationError('Username already exists')


    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')

class UpdateAccountForm(FlaskForm):
    email=StringField('Email' , validators=[InputRequired(), Email(message='Invalid Input') ,Length(max=50)])
    username=StringField('Username' , validators=[InputRequired(), Length(min=4 , max=20)])
    
    submit=SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists')


    def validate_email(self,email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists')


class RequestResetForm(FlaskForm):
    email=StringField('Email' , validators=[InputRequired(), Email(message='Invalid Input') ,Length(max=50)])
    submit=SubmitField('Request Password Reset')

    def validate_email(self , email):
        user=User.query.filter_by(email = email.data).first()

        if user is None :
            raise ValidationError("There is no account with that email")


class ResetPasswordForm(FlaskForm):
    password=PasswordField('New Password' , validators=[InputRequired() , Length(min=8 , max=80)])
    confirm_password=PasswordField('Confirm Password' , validators=[InputRequired() , EqualTo('password')])
    submit=SubmitField('Reset Password')