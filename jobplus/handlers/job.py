from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import current_user

from jobplus.decorators import company_required, seeker_required
from jobplus.forms import JobPublishForm
from jobplus.models import Job, Tag, db

job = Blueprint('job', __name__, url_prefix='/job')


@job.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=12,
        error_out=False
    )
    return render_template('job/index.html', pagination=pagination)


@job.route('/publish', methods=['GET', 'POST'])
@company_required
def publish():
    form = JobPublishForm()
    company = current_user.company
    if form.validate_on_submit():
        form.save(company)
        flash('添加职位成功', 'success')
        return redirect(url_for('user.index'))
    return render_template('job/publish.html', form=form)


@job.route('/update/<int:job_id>', methods=['GET', 'POST'])
@company_required
def update(job_id):
    job = Job.query.get_or_404(job_id)
    form = JobPublishForm(obj=job)
    if form.validate_on_submit():
        form.update(job)
        flash('编辑职位成功', 'success')
        return redirect(url_for('user.index'))
    return render_template('job/update.html', form=form, job_id=job_id)


@job.route('/delete/<int:job_id>', methods=['GET', 'POST'])
@company_required
def delete(job_id):
    job = Job.query.get_or_404(job_id)
    JobPublishForm.delete(job)
    flash('删除职位成功', 'success')
    return redirect(url_for('user.index'))


@job.route('/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html', job=job)


@job.route('/post_resume/<int:job_id>')
@seeker_required
def post_resume(job_id):
    job = Job.query.get_or_404(job_id)
    seeker = current_user.seeker
    job.seekers.append(seeker)
    db.session.add(job)
    db.session.commit()
    flash('投递成功', 'success')
    return redirect(url_for('job.detail', job_id=job_id))


@job.route('/resume_record/<int:job_id>')
@company_required
def resume_record(job_id):
    job = Job.query.get_or_404(job_id)
    page = request.args.get('page', 1, type=int)
    pagination = job.seekers.paginate(
        page=page,
        per_page=10,
        error_out=False
    )
    return render_template('job/resume_recode.html', pagination=pagination,job=job)
