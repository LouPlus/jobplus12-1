from flask import Blueprint, request, redirect, flash
from sqlalchemy import and_

from jobplus.decorators import seeker_required, company_required
from jobplus.models import Resume, db

resume = Blueprint('resume', __name__, url_prefix='/resume')


@resume.route('/post/<int:job_id>/<int:seeker_id>')
@seeker_required
def post(job_id, seeker_id):
    resume = Resume(
        job_id=job_id,
        seeker_id=seeker_id
    )
    db.session.add(resume)
    db.session.commit()
    return redirect(request.referrer)


@resume.route('/interview/<int:job_id>/<int:seeker_id>')
@company_required
def interview(job_id, seeker_id):
    resume = Resume.query.filter(
        and_(
            Resume.job_id == job_id,
            Resume.seeker_id == seeker_id
        )
    ).first()
    resume.set_feedback(2)
    flash('操作成功')
    return redirect(request.referrer)


@resume.route('/reject/<int:job_id>/<int:seeker_id>')
@company_required
def reject(job_id, seeker_id):
    resume = Resume.get(job_id, seeker_id)
    if resume:
        resume.set_feedback(1)
        flash('操作成功')
    else:
        flash('操作失败')
    return redirect(request.referrer)
