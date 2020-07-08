from flask import Flask , render_template , request  , redirect , url_for , flash, request , abort , Blueprint 
from blogpost import db , login_manager 
from blogpost.models import Post
from blogpost.posts.forms import NewPosts
from flask_login import  login_user , logout_user , current_user , login_required

posts=Blueprint('posts' , __name__)


@posts.route("/add_post",methods=["POST","GET"])
@login_required
def new_post():
    form=NewPosts()
    if form.validate_on_submit():
        post=Post(title = form.title.data , content = form.content.data, author = current_user)       
        db.session.add(post)
        db.session.commit()
        flash("New Post has been created successfully ",'success')
        return redirect(url_for('main.posts'))
    else:
        return render_template("new_post.html",form=form)
    return redirect('main.posts')

@posts.route("/add_post/<int:post_id>")
@login_required
def post_with_id(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_with_id.html",posts = post)


@posts.route("/add_post/<int:post_id>/edit",methods=["POST","GET"])
@login_required
def edit(post_id):
    post=Post.query.get_or_404(post_id)
    # if post.author!=current_user:
    #     abort(403)
    form=NewPosts()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Changes were saved successfully",'success')
        return redirect(url_for('posts.post_with_id',post_id = post.id))
    elif request.method=="GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("edit.html",form = form ,post = post)


@posts.route("/add_post/<int:post_id>/delete",methods=["POST"])
def delete_post(post_id):
    post=Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.posts'))
