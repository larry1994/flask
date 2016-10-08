# coding=utf-8


from flask.ext.wtf import Form
from wtforms import StringField,TextAreaField,BooleanField,SelectField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField
from ..models import Role,User

class PostForm(Form):
    title = StringField(u"标题")
    body = PageDownField(u"你在想些什么？",validators=[Required()])
    tag = StringField (u'分类')
    time = StringField(u'日期')
    submit = SubmitField(u'写好啦！')


class CommentForm(Form):
    body = StringField('',validators=[Required()])
    submit = SubmitField(u'评论')
