import os
import re

from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, FileField, \
    SelectField, SelectMultipleField, DateTimeField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL

from jobplus.models import User, Company, db, Seeker, Job, Tag, Education


class BaseForm(FlaskForm):
    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()


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
            role=User.ROLE_SEEKER
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


class SeekerProfileForm(FlaskForm):
    _choices = Education.get_level_choices()
    name = StringField('真实姓名', validators=[DataRequired(), Length(2, 12)])
    phone = StringField('手机号', validators=[DataRequired()])
    age = IntegerField('年纪', validators=[DataRequired()])
    education = SelectField(
        '最高学历',
        choices=_choices,
        coerce=int,
        default=1
    )
    work_year = IntegerField('工作年限', validators=[DataRequired()])
    work_experience = TextAreaField('工作经历', validators=[DataRequired(), Length(10, 250)])
    desc = TextAreaField('自我评价', validators=[DataRequired(), Length(10, 250)])
    submit = SubmitField('提交')

    def save(self, seeker):
        seeker.name = self.name.data
        seeker.phone = self.phone.data
        seeker.work_year = self.work_year.data
        seeker.work_experience = self.work_experience.data
        seeker.desc = self.desc.data
        db.session.add(seeker)
        db.session.commit()

    def validate_phone(self, field):
        if not re.match(r"^1[35678]\d{9}$", field.data):
            raise ValidationError('请填写正确的手机号码')


class ExperienceForm(FlaskForm):
    name = StringField('公司名称', validators=[DataRequired(), Length(2, 12)])
    department = StringField('所属部门', validators=[DataRequired(), Length(2, 12)])
    job_name = StringField('职位名称', validators=[DataRequired(), Length(2, 12)])
    in_time = DateField('入职时间(年-月-日)', validators=[DataRequired()], format='%Y-%m-%d')
    out_time = DateField('离职时间(年-月-日)', format='%Y-%m-%d')
    work_content = TextAreaField('工作内容', validators=[DataRequired(), Length(10, 250)])
    submit = SubmitField('提交')

    def validate_out_time(self, field):
        if field.data:
            delta = field.data - self.in_time.data
            if delta.days <= 0:
                raise ValidationError('离职时间必须比入职时间晚')


class ProjectForm(FlaskForm):
    name = StringField('项目名称', validators=[DataRequired(), Length(2, 12)])
    in_time = DateField('项目开始时间(年-月-日)', validators=[DataRequired()], format='%Y-%m-%d')
    out_time = DateField('项目结束时间(年-月-日)', format='%Y-%m-%d')
    desc = TextAreaField('项目描述', validators=[DataRequired(), Length(10, 250)])
    submit = SubmitField('提交')

    def validate_out_time(self, field):
        if field.data:
            delta = field.data - self.in_time.data
            if delta.days <= 0:
                raise ValidationError('项目结束时间必须比项目开始时间晚')


class EducationForm(FlaskForm):
    _choices = Education.get_level_choices()
    name = StringField('学校名称', validators=[DataRequired(), Length(2, 12)])
    in_time = DateField('入学时间(年-月-日)', validators=[DataRequired()], format='%Y-%m-%d')
    out_time = DateField('毕业时间(年-月-日)', format='%Y-%m-%d')
    level = SelectField(
        '最高学历',
        choices=_choices,
        coerce=int,
        default=1
    )
    pro = StringField('专业名称', validators=[DataRequired(), Length(2, 12)])
    submit = SubmitField('提交')

    def validate_out_time(self, field):
        if field.data:
            delta = field.data - self.in_time.data
            if delta.days <= 0:
                raise ValidationError('毕业时间必须比入学时间晚')


class SeekerResumeForm(FlaskForm):
    resume = FileField('上传简历', validators=[FileRequired()])
    submit = SubmitField('提交')

    def save(self, seeker):
        filename = self.resume.data.filename
        # 存简历文件的问价夹名称
        resume_folder_name = 'resumes'
        # 访问简历文件的url
        file_url = '/resumes/' + filename
        # 本地简历文件的路径
        local_folder = os.path.join(os.path.dirname(current_app.instance_path),
                                    'jobplus',
                                    resume_folder_name)
        # 如果本地不存在存放简历文件的文件夹则创建文件夹
        if not os.path.isdir(local_folder):
            os.mkdir(local_folder)
        # 简历文件存放的本地路径
        local_filename = os.path.join(local_folder,
                                      filename)
        # 将简历文件保存在本地
        self.resume.data.save(local_filename)
        # 设置求职者简历的Url
        seeker.resume = file_url
        # 保存到数据库
        db.session.add(seeker)
        db.session.commit()


class PasswordForm(FlaskForm):
    ori_password = PasswordField('原密码', validators=[DataRequired(), Length(6, 12)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 12)])
    password_repeat = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def save(self, user):
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()


class JobPublishForm(BaseForm):
    name = StringField('职位名称', validators=[DataRequired(), Length(2, 12)])
    _choices = [(getattr(Job, 'SALARY_LEVEL_' + str(i)), getattr(Job, 'SALARY_LEVEL_' + str(i))) for i in range(7)]
    salary = SelectField(
        '薪资范围',
        choices=_choices,
        coerce=str,
        default=getattr(Job, 'SALARY_LEVEL_0')
    )
    addr = StringField('工作地点', validators=[DataRequired(), Length(2, 12)])
    experience = IntegerField('工作经验要求(单位：年)', validators=[DataRequired()])
    desc = TextAreaField('职位详情', validators=[DataRequired()])
    requires = TextAreaField('职位要求', validators=[DataRequired()])
    submit = SubmitField('提交')

    def save(self, company):
        job = Job(
            company=company,
            name=self.name.data,
            salary=self.salary.data,
            addr=self.addr.data,
            experience=self.experience.data,
            desc=self.desc.data,
            requires=self.requires.data
        )

        db.session.add(job)
        db.session.commit()

    def update(self, job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()


class TagForm(BaseForm):
    name = StringField('标签名(2-10)', validators=[DataRequired(), Length(2, 10)])
    submit = SubmitField('提交')

    def save(self, job):
        tag = Tag.query.filter_by(name=self.name.data).first()
        if not tag:
            tag = Tag(name=self.name.data)
        job.tags.append(tag)
        db.session.add(tag)
        db.session.add(job)
        db.session.commit()

    def save_self(self):
        tag = Tag(name=self.name.data)
        db.session.add(tag)
        db.session.commit()

    @staticmethod
    def delete(job, tag):
        job.tags.remove(tag)
        db.session.add(job)
        db.session.commit()


class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称', validators=[DataRequired(), Length(2, 12)])
    addr = StringField('地址', validators=[DataRequired()])
    website = StringField('企业网址')
    slogan = StringField('一句话介绍', validators=[DataRequired()])
    desc = TextAreaField('详细介绍', validators=[DataRequired()])
    submit = SubmitField('提交')

    def save(self, company):
        self.populate_obj(company)
        db.session.add(company)
        db.session.commit()


class CompanyLogoForm(FlaskForm):
    logo = FileField('上传企业头像', validators=[FileRequired()])
    submit = SubmitField('提交')

    def save(self, company):
        filename = self.logo.data.filename
        # 存企业头像文件的文件夹名称
        logo_folder_name = 'logo'
        # 访问头像文件的url
        file_url = '/logos/' + filename
        # 本地头像文件的路径
        local_folder = os.path.join(os.path.dirname(current_app.instance_path),
                                    'jobplus',
                                    logo_folder_name)
        # 如果本地不存在存放头像文件的文件夹则创建文件夹
        if not os.path.isdir(local_folder):
            os.mkdir(local_folder)
        # 头像文件存放的本地路径
        local_filename = os.path.join(local_folder,
                                      filename)
        # 将头像文件保存在本地
        self.logo.data.save(local_filename)
        # 设置头像的Url
        company.logo = file_url
        # 保存到数据库
        db.session.add(company)
        db.session.commit()


class UserForm(BaseForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    name = StringField('姓名或企业名', validators=[DataRequired(), Length(2, 12)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 12)])
    password_repeat = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    _choices = ((User.ROLE_SEEKER, '用户'), (User.ROLE_COMPANY, '企业'))
    role = SelectField(
        '角色',
        choices=_choices,
        coerce=int,
        default=getattr(Job, 'SALARY_LEVEL_0')
    )
    submit = SubmitField('提交')

    def save(self):
        user = User(
            email=self.email.data,
            password=self.password.data,
            role=self.role.data
        )
        db.session.add(user)
        #

        if user.is_company:
            company = Company(
                user=user,
                name=self.name.data
            )
            db.session.add(company)
        elif user.is_seeker:
            seeker = Seeker(
                user=user,
                name=self.name.data
            )
            db.session.add(seeker)

        db.session.commit()


class UserUpdateForm(BaseForm):
    name = StringField('姓名或企业名', validators=[DataRequired(), Length(2, 12)])
    password = PasswordField('密码(不填不改)')
    submit = SubmitField('提交')

    def save(self, user):
        if self.password.data:
            user.password = self.password.data
            db.session.add(user)
        if user.is_seeker:
            user.seeker.name = self.name.data
            db.session.add(user.seeker)
        elif user.is_company:
            user.company.name = self.name.data
            db.session.add(user.company)
        db.session.commit()
