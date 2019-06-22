from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user

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
def logout():
    logout_user()
    flash('退出成功！', 'success')
    return redirect(url_for('.index'))
