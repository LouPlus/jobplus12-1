from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base, UserMixin):
    # 求职者角色
    ROLE_SEEKER = 10
    # 企业角色
    ROLE_COMPANY = 20
    # 管理员角色
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    # 邮箱
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    # 密码
    __password = db.Column('password', db.String(256), nullable=False)
    # 角色
    role = db.Column(db.SmallInteger, nullable=False)

    seeker = db.relationship('Seeker', uselist=False)
    company = db.relationship('Company', uselist=False)

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, pwd):
        if len(pwd.strip()):
            self.__password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.__password, pwd)

    @property
    def is_seeker(self):
        return self.role == self.ROLE_SEEKER

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def role_text(self):
        if self.is_admin:
            return '管理员'
        elif self.is_company:
            return '企业'
        else:
            return '求职者'

    @property
    def name(self):
        if self.seeker:
            return self.seeker.name
        elif self.company:
            return self.company.name


class Seeker(Base):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User')
    # 姓名
    name = db.Column(db.String(64), nullable=False)
    # 电话
    phone = db.Column(db.String(64))
    # 工作年限
    work_year = db.Column(db.SmallInteger)
    # 简历文件地址
    resume = db.Column(db.String(256))
    # 工作经历
    work_experience = db.Column(db.TEXT)
    # 自我描述
    desc = db.Column(db.TEXT)


class Company(Base):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User')
    # 名称
    name = db.Column(db.String(64), nullable=False)
    # 企业详情
    desc = db.Column(db.TEXT)
    # 企业地址
    addr = db.Column(db.String(128))
    # 企业网站地址
    website = db.Column(db.String(128))
    # 企业logo
    logo = db.Column(db.String(256))
    # 一句话简介
    slogan = db.Column(db.String(64))


# 工作标签中间表
job_tag = db.Table(
    'job_tag',
    Base.metadata,
    db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'), primary_key=True, ),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True, )
)


class Job(Base):
    SALARY_LEVEL_0 = '面议'
    SALARY_LEVEL_1 = '2k-5k'
    SALARY_LEVEL_2 = '5k-10k'
    SALARY_LEVEL_3 = '10k-15k'
    SALARY_LEVEL_4 = '15k-25k'
    SALARY_LEVEL_5 = '25k-50k'
    SALARY_LEVEL_6 = '50以上'

    id = db.Column(db.Integer, primary_key=True)
    # 发布工作公司ID
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
    company = db.relationship('Company', uselist=False, backref='jobs')
    # 名称
    name = db.Column(db.String(64), nullable=False, index=True)
    # 工资范围
    salary = db.Column(db.String(64), nullable=False, index=True, default=SALARY_LEVEL_0)
    # 工作地址
    addr = db.Column(db.String(64), nullable=False, index=True)
    # 工作经验要求
    experience = db.Column(db.SmallInteger)
    # 工作描述
    desc = db.Column(db.TEXT)
    # 工作要求
    requires = db.Column(db.TEXT)
    tags = db.relationship('Tag', secondary=job_tag, back_populates='jobs')


class Tag(Base):
    id = db.Column(db.Integer, primary_key=True)
    # 标签名称
    name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    jobs = db.relationship('Job', secondary=job_tag, back_populates='tags')
