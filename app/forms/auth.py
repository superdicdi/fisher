from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, ValidationError

from app.models.user import User

__author__ = "TuDi"
__date__ = "2018/12/21 下午2:12"


class RegisterForm(Form):
    email = StringField(
        description="邮箱",
        validators=[
            DataRequired(),
            Length(8, 64),
            Email(message="电子邮箱格式不对")
        ]
    )
    nickname = StringField(description='昵称', validators=[
        DataRequired("昵称不能为空"), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    password = PasswordField(description='密码', validators=[
        DataRequired("密码不能为空"), Length(6, 20)])

    def validate_email(self, field):
        email = field.data
        data = User.query.filter_by(email=email).count()
        if data:
            raise ValidationError("邮箱已经注册")


    def validate_nickname(self, field):
        nickname = field.data
        data = User.query.filter_by(nickname=nickname).count()
        if data:
            raise ValidationError("昵称已经存在")


class LoginForm(Form):

    nickname = StringField(description='昵称', validators=[
        DataRequired("昵称不能为空"), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    password = PasswordField(description='密码', validators=[
        DataRequired("密码不能为空"), Length(6, 20)])


