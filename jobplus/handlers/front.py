import os

from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory, current_app, make_response
from flask_login import login_user, logout_user, login_required

from jobplus.forms import RegCompanyFrom, RegSeekerForm, LoginForm

front = Blueprint('front', __name__)


@front.route('/')
def index():
    return render_template('index.html')


@front.route('/register/company', methods=['GET', 'POST'])
def reg_company():
    form = RegCompanyFrom()
    if form.validate_on_submit():
        form.register()
        flash('注册成功', 'success')
        return redirect(url_for('.login'))
    return render_template('front/reg_company.html', form=form)


@front.route('/register/seeker', methods=['GET', 'POST'])
def reg_seeker():
    form = RegSeekerForm()
    if form.validate_on_submit():
        form.register()
        flash('注册成功', 'success')
        return redirect(url_for('.login'))
    return render_template('front/reg_seeker.html', form=form)


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        if user:
            login_user(user, form.remember_me.data)
            return redirect(url_for('.index'))
    return render_template('front/login.html', form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功！', 'success')
    return redirect(url_for('.index'))


@front.route('/resumes/<filename>')
@login_required
def resume(filename):
    resume_folder_name = 'resumes'
    local_folder = os.path.join(os.path.dirname(current_app.instance_path),
                                'jobplus',
                                resume_folder_name)
    response = make_response(send_from_directory(local_folder, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response
