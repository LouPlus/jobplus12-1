from flask import Blueprint, render_template, request, redirect, flash, url_for

from jobplus.decorators import seeker_required
from jobplus.forms import ExperienceForm, ProjectForm
from jobplus.models import Experiences, Seeker, Project

project = Blueprint('project', __name__, url_prefix='/project')


@project.route('/add/<int:seeker_id>', methods=['GET', 'POST'])
@seeker_required
def add(seeker_id):
    seeker = Seeker.query.get_or_404(seeker_id)
    form = ProjectForm()
    if form.validate_on_submit():
        Project.add_for_seeker(form, seeker)
        flash('添加成功', 'success')
        return redirect(url_for('seeker.profile', seeker_id=seeker_id))
    return render_template('project/form.html', form=form)


@project.route('/update/<int:project_id>', methods=['GET', 'POST'])
@seeker_required
def update(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.update(form)
        flash('修改成功', 'success')
        return redirect(url_for('seeker.profile', seeker_id=project.seeker_id))
    return render_template('project/form.html', form=form)


@project.route('/delete/<int:project_id>')
@seeker_required
def delete(project_id):
    project = Project.query.get_or_404(project_id)
    Project.delete(project)
    flash('删除成功', 'success')
    return redirect(request.referrer)
