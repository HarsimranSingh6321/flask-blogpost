from flask import Flask , render_template , request  , redirect , url_for , flash, request , abort , Blueprint 
from blogpost import db , login_manager
from blogpost.models import User , Post
from blogpost.users.forms import (LoginForm , RegisterForm 
                        ,UpdateAccountForm , RequestResetForm , ResetPasswordForm )
from blogpost import Bootstrap , login_manager , mail
from flask_login import login_required , login_user , logout_user , current_user 
from werkzeug.security import generate_password_hash , check_password_hash
from flask_mail import Message
from blogpost.users.utils import send_reset_email

users=Blueprint('users' , __name__)

@login_manager.user_loader
def load_user(post_id):
    user=User.query.get(int(post_id))
    return user

@users.route('/register',methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.posts'))
    form =RegisterForm()
    if form.validate_on_submit():
        
        hashed_pass=generate_password_hash(form.password.data  ,method='sha256')
        user=User(username=form.username.data , email=form.email.data , password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created successfully', category='success')
        return redirect(url_for('users.login'))
    return render_template("signup.html",form=form)

@users.route('/login',methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.posts'))
    form =LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password , form.password.data):
            login_user(user,remember=form.remember.data)
            flash("You have been logged in successfully","success")
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.posts'))
        else:
            flash('Please check your username or password','danger')

    return render_template('login.html',form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.posts'))

@users.route("/account",methods=["GET","POST"])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated successfully",'success')
        return redirect(url_for('users.account'))
    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
    return render_template("account.html",form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1 , type=int)
    user=User.query.filter_by(username = username).first_or_404()
    all_posts=Post.query.filter_by(author = user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page = page , per_page = 3)
    return render_template("user_posts.html" , posts = all_posts , user = user)

@users.route("/reset_password",methods=["GET","POST"])
def request_token():
    if current_user.is_authenticated:
        return redirect(url_for('main.posts'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("A link has been sent to the email id provided by you , folow that link to reset your password",'info')
        return redirect(url_for('users.login'))

    return render_template("reset_request.html" , form=form)
        

@users.route("/reset_password/<token>",methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.posts'))

    user=User.verify_reset_token(token)
    if not user:
        flash("That is an invalid token or expired token", 'warning' )
        return redirect(url_for('users.request_token'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been changed successfully",'success')
        return redirect(url_for('users.login'))

    return render_template("reset_password.html" , form = form , token = token)
