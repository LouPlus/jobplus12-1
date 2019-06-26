from flask import Blueprint, render_template, request, flash, redirect, url_for

from jobplus.decorators import company_required, company_admin_required
from jobplus.forms import TagForm
from jobplus.models import Job, Tag

tag = Blueprint('tag', __name__, url_prefix='/tag')


@tag.route('/job/<int:job_id>')
@company_admin_required
def job_tag(job_id):
    job = Job.query.get_or_404(job_id)
    page = request.args.get('page', 1, type=int)
    pagination = job.tags.order_by(Tag.created_at.desc()).paginate(
        per_page=3,
        page=page,
        error_out=False
    )
    return render_template('tag/list.html', pagination=pagination, job=job)


@tag.route('/job/<int:job_id>/create', methods=['POST'])
@company_admin_required
def job_tag_create(job_id):
    tag_name = request.form.get('name', None)
    if not tag_name:
        flash('标签名不能为空', 'danger')
        return redirect(request.referrer)
    tag = Tag.query.filter_by(name=tag_name).first()
    job = Job.query.get_or_404(job_id)
    if not tag:
        tag = Tag(name=tag_name)
    Job.add_tag(job, tag)
    flash('添加标签成功', 'success')
    return redirect(url_for('tag.job_tag', job_id=job_id))


# job = Job.query.get_or_404(job_id)
# form = TagForm()
# if form.validate_on_submit():
#     form.save(job)
#     flash('添加标签成功', 'success')
#     return redirect(url_for('.job_tag', job_id=job_id))
# return render_template('tag/form.html', job=job, form=form)


@tag.route('/job/<int:job_id>/delete/<int:tag_id>')
@company_admin_required
def job_tag_delete(job_id, tag_id):
    job = Job.query.get_or_404(job_id)
    tag = Tag.query.get_or_404(tag_id)
    TagForm.delete(job, tag)
    flash('删除成功', 'success')
    return redirect(url_for('.job_tag', job_id=job_id))
