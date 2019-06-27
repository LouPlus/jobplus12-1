from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    PER_PAGE = 10
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def query_pagination(cls, query, page, per_page=10):
        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )


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
    # 账户状态 禁用或启用
    enable = db.Column(db.Boolean, default=True)

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
        if self.is_seeker:
            return self.seeker.name
        elif self.is_company:
            return self.company.name
        else:
            return '管理员'

    @staticmethod
    def status(user, status):
        user.enable = status
        db.session.add(user)
        db.session.commit()


class Resume(Base):
    # 简历未处理
    RESUME_UNTREATED = 0
    # 简历不合适
    RESUME_NOT_SUIT = 1
    # 简历通过邀请面试
    RESUME_INTERVIEW = 2

    id = db.Column(db.Integer, primary_key=True)
    seeker_id = db.Column('seeker_id', db.Integer, db.ForeignKey('seeker.id', ondelete='CASCADE'))
    job_id = db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
    freed_back = db.Column('freed_back', db.Integer, default=RESUME_UNTREATED)

    seeker = db.relationship('Seeker', uselist=False, backref='resumes')
    job = db.relationship('Job', uselist=False, backref='resumes')

    @property
    def feed_back_text(self):
        map = {
            self.RESUME_UNTREATED: '未处理',
            self.RESUME_NOT_SUIT: '不合适',
            self.RESUME_INTERVIEW: '面试',
        }
        return map.get(self.freed_back)

    def set_feedback(self, feedback):
        self.freed_back = feedback
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get(cls, job_id, seeker_id):
        resume = Resume.query.filter(
            and_(
                Resume.job_id == job_id,
                Resume.seeker_id == seeker_id
            )
        ).first()
        return resume

    @classmethod
    def get_by_job_and_feedback(cls, job_id, feedback):
        return Resume.query.filter(
            and_(
                Resume.job_id == job_id,
                Resume.freed_back == feedback
            )
        )


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

    @property
    def email(self):
        return self.user.email

    @property
    def role_text(self):
        return self.user.role_text

    def have_posted_job(self, job_id):
        return Resume.query.filter(and_(
            Resume.seeker_id == self.id,
            Resume.job_id == job_id
        )).first()


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
    logo = db.Column(db.String(256), default='//www.lgstatic.com/thumbnail_300x300/images/logo_default.png')
    # 一句话简介
    slogan = db.Column(db.String(64))

    @property
    def email(self):
        return self.user.email

    @property
    def role_text(self):
        return self.user.role_text


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
    SALARY_LEVEL_6 = '50k以上'

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
    # 是否上线 默认是
    online = db.Column(db.Boolean, default=True, index=True)

    tags = db.relationship('Tag', secondary=job_tag, back_populates='jobs', lazy='dynamic')

    @property
    def experience_text(self):
        if self.experience:
            return str(self.experience) + '年经验'
        else:
            return '经验不限'

    @property
    def publish_time(self):
        time = (datetime.now() - self.updated_at)
        days = time.days
        seconds = time.seconds
        time_str = ''
        if days:
            time_str = str(days) + '天之前发布'
        else:
            hours = int(seconds / 3600)
            if hours:
                time_str = str(hours) + '小时之前发布'
            else:
                time_str = '刚刚发布'
        return time_str

    @staticmethod
    def add_tag(job, tag):
        job.tags.append(tag)
        db.session.add(job)
        db.session.add(tag)
        db.session.commit()

    @classmethod
    def get_salary_choices(cls):
        return (getattr(cls, 'SALARY_LEVEL_' + str(i)) for i in range(7))

    @property
    def online_text(self):
        return '上线' if self.online else '下线'

    def set_status(self, status):
        self.online = status
        db.session.add(self)
        db.session.commit()


class Tag(Base):
    id = db.Column(db.Integer, primary_key=True)
    # 标签名称
    name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    jobs = db.relationship('Job', secondary=job_tag, back_populates='tags', lazy='dynamic')

    @staticmethod
    def get_have_jobs_count_top_n(n):
        """
        获取被职位引用数最多的前N个标签
        :param n: 
        :return: [标签ID,标签名称,标签被职位引用个数] 
        """""
        sql = 'select tag.id, tag.name, count(job_tag.job_id) as jobs from tag join job_tag ' \
              'on tag.id = job_tag.tag_id ' \
              'group by tag.id ' \
              'order by jobs desc ' \
              'limit 0,{};'.format(n)
        tags = tuple(db.engine.execute(sql))
        return tags
