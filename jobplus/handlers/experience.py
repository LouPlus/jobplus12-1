from flask import Blueprint, render_template, request, redirect, flash, url_for

from jobplus.decorators import seeker_required
from jobplus.forms import ExperienceForm
from jobplus.models import Experiences, Seeker

experience = Blueprint('experience', __name__, url_prefix='/experience')


@experience.route('/add/<int:seeker_id>', methods=['GET', 'POST'])
@seeker_required
def add(seeker_id):
    seeker = Seeker.query.get_or_404(seeker_id)
    form = ExperienceForm()
    if form.validate_on_submit():
        Experiences.add_for_seeker(form, seeker)
        flash('添加成功', 'success')
        return redirect(url_for('seeker.profile', seeker_id=seeker_id))
    return render_template('experience/form.html', form=form)


@experience.route('/update/<int:experience_id>', methods=['GET', 'POST'])
@seeker_required
def update(experience_id):
    experience = Experiences.query.get_or_404(experience_id)
    form = ExperienceForm(obj=experience)
    if form.validate_on_submit():
        experience.update(form)
        flash('修改成功', 'success')
        return redirect(url_for('seeker.profile', seeker_id=experience.seeker_id))
    return render_template('experience/form.html', form=form)


@experience.route('/delete/<int:experience_id>')
@seeker_required
def delete(experience_id):
    experience = Experiences.query.get_or_404(experience_id)
    Experiences.delete(experience)
    flash('删除成功', 'success')
    return redirect(request.referrer)
