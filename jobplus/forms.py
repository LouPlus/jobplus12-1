from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from jobplus.models import User, Company, db, Seeker


class RegCompanyFrom(FlaskForm):
    name = StringField('企业名称', validators=[DataRequired(), Length(3, 12)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 12)])
    password_repeat = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def register(self):
        user = User(
            email=self.email.data,
            password=self.password.data,
            role=User.ROLE_COMPANY
        )

        company = Company(
            user=user,
            name=self.name.data
        )
        db.session.add(user)
        db.session.add(company)
        db.session.commit()


class RegSeekerForm(FlaskForm):
    name = StringField('真实姓名', validators=[DataRequired(), Length(2, 12)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 12)])
    password_repeat = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def register(self):
        user = User(
            email=self.email.data,
            password=self.password.data,
            role=User.ROLE_COMPANY
        )

        seeker = Seeker(
            user=user,
            name=self.name.data
        )
        db.session.add(user)
        db.session.add(seeker)
        db.session.commit()


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 12)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        user = self.get_user()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

    def get_user(self):
        user = User.query.filter_by(email=self.email.data).first()
        return user
