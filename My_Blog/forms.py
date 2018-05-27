from flask_wtf import FlaskForm as Form
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):#登录表单
    username = StringField(validators=[DataRequired(),Length(max=15)])
    password = StringField(validators=[DataRequired(),Length(max=15)])
    rememmber_me = BooleanField('remember me',default=False)
    submit = SubmitField('Login')

class SignUpForm(Form):#注册表单
    username = StringField(validators=[DataRequired(), Length(max=15)])
    password = StringField(validators=[DataRequired(), Length(max=15)])
    submit = SubmitField('Sign Up')

class WriteForm(Form):#写博客表单
    title = StringField('title',validators=[DataRequired()])
    content = TextAreaField('content',validators=[DataRequired()])
    submit = SubmitField('提交')

class EditUserForm(Form):
     name = StringField('username',validators=[DataRequired()])
     profession = StringField('profession')
     year = StringField('year')
     city = StringField("city")