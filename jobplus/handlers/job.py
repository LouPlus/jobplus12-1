from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy import or_, and_

from jobplus.decorators import company_required, seeker_required, company_admin_required
from jobplus.forms import JobPublishForm
from jobplus.models import Job, Tag, db, Company, job_tag, Resume

job = Blueprint('job', __name__, url_prefix='/job')


@job.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    query = Job.query.filter_by(online=True).order_by(Job.updated_at.desc())
    keyword = request.args.get('keyword') or request.form.get('keyword')
    # 如果是点的搜索下面的标签链接过来的话会带有这个参数
    tag_id = request.args.get('tag_id', None, int)
    # 获取被职位引用数最多的前5个标签
    tags = Tag.get_have_jobs_count_top_n(5)
    # 工资范围选项
    salarys = Job.get_salary_choices()
    query_salary = request.args.get('salary', None)

    # 去掉前后空格
    if isinstance(keyword, str):
        keyword = keyword.strip()
    # 关键字搜索
    if keyword:
        query = Job.query.join(Company).filter(
            and_(
                Job.online,
                or_(
                    Job.name.contains(keyword),
                    Company.name.contains(keyword)
                )
            )
        ).order_by(Job.updated_at.desc())
        page = 1
    elif tag_id:
        # 标签职位查询
        query = Job.query.join(Job.tags).filter(and_(
            Tag.id == tag_id,
            Job.online
        ))
    elif query_salary:
        query = Job.query.filter(and_(
            Job.online,
            Job.salary == query_salary
        ))

    pagination = Job.query_pagination(query, page, per_page=12)
    return render_template('job/index.html', pagination=pagination, tags=tags, salarys=salarys)


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
    i_publish_this = False
    if current_user.is_authenticated and current_user.is_company and job.company_id == current_user.company.id:
        i_publish_this = True

    have_posted_job = False
    if current_user.is_authenticated and current_user.is_seeker:
        have_posted_job = current_user.seeker.have_posted_job(job_id)
    return render_template('job/detail.html', job=job, have_posted_job=have_posted_job, i_publish_this=i_publish_this)


@job.route('/resume_record/<int:job_id>')
@company_required
def resume_record(job_id):
    job = Job.query.get_or_404(job_id)
    page = request.args.get('page', 1, type=int)
    feedback = request.args.get('feedback', 0, type=int)
    query = Resume.get_by_job_and_feedback(job_id, feedback)
    pagination = Resume.query_pagination(query, page)
    return render_template('job/resume_recode.html', pagination=pagination, job=job, feedback=feedback)


@job.route('/offline/<int:job_id>')
@company_admin_required
def offline(job_id):
    job = Job.query.get_or_404(job_id)
    job.set_status(False)
    return redirect(request.referrer)


@job.route('/online/<int:job_id>')
@company_admin_required
def online(job_id):
    job = Job.query.get_or_404(job_id)
    job.set_status(True)
    return redirect(request.referrer)
