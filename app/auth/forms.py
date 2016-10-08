# coding=utf-8


from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User



class LoginForm(Form):
    email = StringField(u'邮箱',validators=[Required(),Length(1,64),Email()])
    password = PasswordField(u'密码',validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class RegistrationForm(Form):
    email = StringField(u'邮箱',validators=[Required(),Length(1,64),Email()])
    username = StringField(u'用户名',validators=[Required(),Length(1,64),
                                             Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                    u'用户名只能以字母开头，并且只能包含字母和数字')])
    password = PasswordField(u'密码',validators=[
        Required(),EqualTo(u'password2',message=u'两次输入的密码不一样')
    ])
    password2 = PasswordField(u'确认密码',validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册过了')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'这个用户名已经有人使用啦！')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'旧密码',validators=[Required()])
    password = PasswordField(u'新密码',validators=[Required(),
                                               EqualTo('password2',message=u'两次输入的密码不匹配')])
    password2 = PasswordField(u'确认密码',validators=[Required()])
    submit = SubmitField(u'更新密码')

class PasswordResetRequestForm(Form):
    email = StringField(u'邮件',validators=[Required(),Length(1,64),
                                         Email()])
    submit = SubmitField(u'提交')


class PasswordResetForm(Form):
    email = StringField(u'邮箱',validators=[Required(),Length(1,64),
                                         Email()])
    password = StringField(u'新密码',valitadors=[
        Required(),EqualTo('password2',message=u'两次输入的密码不匹配')])
    password2 = PasswordField(u'确认密码',validators=[Required()])
    submit = SubmitField(u'提交')

    def validators_email(self,field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'邮件地址错误！')



class ChangeEmailForm(Form):
    email = StringField(u'新邮件',validators=[Required(),Length(1,64),
                                          Email()])
    password = PasswordField(u'密码',validators=[Required()])
    submit = SubmitField(u'更新邮件地址')

    def validators_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮件已经被注册过了')