# coding=utf-8

from flask import render_template,redirect,request,url_for,flash,abort,current_app
from flask.ext.login import login_required,current_user
from . import main
from .forms import PostForm,CommentForm
from .. import db
from ..models import Permission,Post,Role,User,Comment



@main.route('/',methods=['GET','POST'])
def index():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=10,error_out=False
    )
    posts = pagination.items
    return render_template('index.html',posts=posts,pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1,type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page,per_page=10,error_out=False)
    posts = pagination.items
    return render_template('index.html',user=user,posts=posts,
                           pagination=pagination)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if current_user.can(Permission.COMMENT) and form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)



@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    #if current_user != post.author and \
        #    not current_user.can(Permission.ADMINISTER):
        #abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data
        post.tag = form.tag.data
        post.time = form.time.data
        db.session.add(post)
        db.session.commit()
        flash(u'文章修改好啦！')
        return redirect(url_for('.post',id=post.id))
    form.body.data = post.body
    form.tag.data = post.tag
    form.title.data = post.title
    form.time.data = post.time
    return render_template('edit_post.html',form=form)

@main.route('/tags/<tag>',methods=['GET'])
def tag(tag):
    posts=Post.query.filter_by(tag=tag)
    return render_template("category_search.html",posts=posts)

@main.route('/write',methods=['GET','POST'])
@login_required
def write():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,
                    title=form.title.data,
                    tag=form.tag.data,
                    time=form.time.data
                    )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('write.html',form=form)
