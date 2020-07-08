from flask import url_for
from flask_mail import Message
from blogpost import mail
from blogpost.models import User

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request',
                sender = 'noreply@gmail.com',
                recipients=[user.email] )
    msg.body = f'''To Reset your Password visit the folowing link : 
{url_for('users.reset_token', token = token , _external = True)}
If you didn't make this request, then ignore it , no changes will be made
'''
    mail.send(msg)