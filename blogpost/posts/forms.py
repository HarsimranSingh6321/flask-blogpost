from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , BooleanField , SubmitField, ValidationError , TextAreaField
from wtforms.validators import InputRequired , Length , email , EqualTo 
from wtforms.validators import Email
from blogpost import Bootstrap


class NewPosts(FlaskForm):
    title=StringField('Title' , validators=[InputRequired(),Length(min=1)])
    content=TextAreaField('Content' , validators=[InputRequired(), Length(min=1)])
    submit=SubmitField('Submit')