from flask import Blueprint, render_template, request, flash, redirect, url_for

from jobplus.decorators import company_required
from jobplus.forms import TagForm
from jobplus.models import Job, Tag

tag = Blueprint('tag', __name__, url_prefix='/tag')


@tag.route('/<int:job_id>')
@company_required
def company_tag(job_id):
    job = Job.query.get_or_404(job_id)
    tags = job.tags
    return render_template('tag/list.html', tags=tags, job=job)


@tag.route('/<int:job_id>/create', methods=['GET', 'POST'])
@company_required
def company_tag_create(job_id):
    job = Job.query.get_or_404(job_id)
    form = TagForm()
    if form.validate_on_submit():
        form.save(job)
        flash('添加标签成功', 'success')
        return redirect(url_for('.company_tag', job_id=job_id))
    return render_template('tag/form.html', job=job, form=form)


@tag.route('/<int:job_id>/delete/<int:tag_id>')
@company_required
def company_tag_delete(job_id, tag_id):
    job = Job.query.get_or_404(job_id)
    tag = Tag.query.get_or_404(tag_id)
    TagForm.delete(job, tag)
    flash('删除成功', 'success')
    return redirect(url_for('.company_tag', job_id=job_id))
