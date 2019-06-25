import json
import os
import random
from faker import Faker

faker = Faker()

from jobplus.models import User, Company, db, Job


def iter_users():
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'companys.json')) as f:
        companys = json.load(f)
    for i, company in enumerate(companys):
        user = User(
            email='test' + str(i) + '@qq.com',
            password='111111',
            role=User.ROLE_COMPANY
        )
        company = Company(
            user=user,
            name=company.get('name'),
            desc=company.get('desc'),
            addr=company.get('addr'),
            logo=company.get('logo'),
            slogan=company.get('slogan'),
        )
        yield user, company


def iter_jobs(companys):
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'job.json')) as f:
        jobs = json.load(f)

    for job in jobs:
        yield Job(
            name=job.get('name'),
            addr=job.get('addr'),
            experience=random.randint(0, 5),
            desc=faker.sentence(),
            requires=faker.sentence(),
            salary=getattr(Job, 'SALARY_LEVEL_' + str(random.randint(0, 5))),
            company=random.choice(companys)
        )


def run():
    companys = []
    for user, company in iter_users():
        db.session.add(user)
        db.session.add(company)
        companys.append(company)

    for job in iter_jobs(companys):
        db.session.add(job)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
