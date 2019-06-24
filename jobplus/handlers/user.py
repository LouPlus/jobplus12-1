from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, logout_user

from jobplus.forms import PasswordForm
from jobplus.models import User, Job

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
@login_required
def index():
    if current_user.is_seeker:
        page = request.args.get('page', 1, type=int)
        pagination = current_user.seeker.posted_jobs.paginate(
            page=page,
            per_page=10,
            error_out=False
        )
        return render_template('seeker/index.html', pagination=pagination)
    elif current_user.is_company:
        company = current_user.company
        page = request.args.get('page', 1, type=int)
        pagination = Job.query.filter_by(company_id=current_user.company.id).paginate(
            page=page,
            per_page=10,
            error_out=False
        )
        return render_template('company/profile.html', pagination=pagination, company=company)


@user.route('/password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def password(user_id):
    user = User.query.get_or_404(user_id)
    form = PasswordForm()
    if form.validate_on_submit():
        if not user.check_password(form.ori_password.data):
            flash('原密码错误，请重新输入', 'danger')
            return redirect(url_for('user.password', user_id=user_id))
        else:
            form.save(user)
            logout_user()
            flash('修改密码成功,请重新登录', 'success')
            return redirect(url_for('front.login'))
    return render_template('user/password.html', form=form)
