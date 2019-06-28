from flask import Blueprint, render_template, request, redirect, flash, url_for

from jobplus.decorators import seeker_required
from jobplus.forms import ExperienceForm, EducationForm
from jobplus.models import Experiences, Seeker, Education

education = Blueprint('education', __name__, url_prefix='/education')


@education.route('/add/<int:seeker_id>', methods=['GET', 'POST'])
@seeker_required
def add(seeker_id):
    seeker = Seeker.query.get_or_404(seeker_id)
    form = EducationForm()
    if form.validate_on_submit():
        Education.add_for_seeker(form, seeker)
        flash('添加成功', 'success')
        return redirect(url_for('seeker.profile', seeker_id=seeker_id))
    return render_template('education/form.html', form=form)


@education.route('/update/<int:education_id>', methods=['GET', 'POST'])
@seeker_required
def update(education_id):
    education = Education.query.get_or_404(education_id)
    form = EducationForm(obj=education)
    if form.validate_on_submit():
        education.update(form)
        flash('修改成功', 'success')
        return redirect(url_for('seeker.profile', seeker_id=education.seeker_id))
    return render_template('education/form.html', form=form)


@education.route('/delete/<int:education_id>')
@seeker_required
def delete(education_id):
    education = Education.query.get_or_404(education_id)
    Experiences.delete(education)
    flash('删除成功', 'success')
    return redirect(request.referrer)
