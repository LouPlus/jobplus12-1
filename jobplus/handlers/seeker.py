from flask import Blueprint, render_template, flash, redirect, url_for

from jobplus.decorators import seeker_required, company_required, company_admin_required, company_seeker_required
from jobplus.forms import SeekerProfileForm, SeekerResumeForm
from jobplus.models import Seeker

seeker = Blueprint('seeker', __name__, url_prefix='/seeker')


@seeker.route('/profile/<int:seeker_id>', methods=['GET', 'POST'])
@seeker_required
def profile(seeker_id):
    user = Seeker.query.get_or_404(seeker_id)
    form = SeekerProfileForm(obj=user)
    if form.validate_on_submit():
        user.update(form)
        flash('保存成功', 'success')
        return redirect(url_for('user.index'))
    return render_template('seeker/profile.html', form=form, user=user)


@seeker.route('/resume/<int:seeker_id>', methods=['GET', 'POST'])
@seeker_required
def resume(seeker_id):
    user = Seeker.query.get_or_404(seeker_id)
    form = SeekerResumeForm()
    if form.validate_on_submit():
        form.save(user)
        flash('保存成功', 'success')
        return redirect(url_for('user.index'))
    return render_template('seeker/resume.html', form=form)


@seeker.route('/detail/<int:seeker_id>')
@company_seeker_required
def detail(seeker_id):
    seeker = Seeker.query.get_or_404(seeker_id)
    return render_template('seeker/detail.html', seeker=seeker)
