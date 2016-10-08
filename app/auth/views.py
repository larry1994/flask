# coding=utf-8


from flask import render_template,redirect,request,url_for,flash
from flask.ext.login import login_user,logout_user,login_required,\
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm,RegistrationForm,ChangePasswordForm,\
    ChangeEmailForm,PasswordResetRequestForm,PasswordResetForm

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或者密码输错了，再给你一次机会好了 ╮(￣▽￣)╭')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'你已经成功退出账号了')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,u'确认账号','auth/email/confirm',user=user,token=token)
        flash(u'确认账号的邮件已经发往你的邮箱，请点击邮件里的链接进行确认')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.html'))
    if current_user.confirm(token):
        flash(u'你已经确认了账号，现在可以开始使用了')
    else:
        flash(u'确认账号的链接已失效，请重新申请确认邮件')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,u'确认账号',
               'auth/email/confirm',user=current_user,token=token)
    flash(u'新的邮件已经发送到你的邮箱啦！')
    return redirect(url_for('main.index'))

@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'密码已修改')
            return redirect(url_for('main.index'))
        else:
            flash(u'密码输错啦！！')
    return render_template("auth/change_password.html",form=form)

@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email,u'重置密码',
                       'auth/email/reset_password',
                       user=user,token=token,
                       next=request.args.get('next'))
        flash(u'重置密码的邮件已发到你的邮箱')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token,form.password.data):
            flash(u'你的密码已更改')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html',form=form)


@auth.route('/change-email',methods=['GET','POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email,u'确认你的邮件地址',
                       'auth/email/change_email',
                       user=current_user,token=token)
            flash(u'一份确认邮件地址的邮件已经发送到你的邮箱，请查收。')
            return redirect(url_for('main.index'))
        else:
            flash(u'邮件地址或者密码输错啦！')
    return render_template('auth/change_email.html',form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash(u'你的新邮件已成功更改')
    else:
        flash(u'出现错误，请重新申请确认邮件！')
    return redirect(url_for('main.index'))

