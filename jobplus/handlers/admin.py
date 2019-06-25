from flask import Blueprint, redirect, url_for, render_template, request, flash

from jobplus.decorators import admin_required
from jobplus.forms import UserForm, UserUpdateForm, BaseForm, TagForm
from jobplus.models import User, Job, Tag, Seeker, Company

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return redirect(url_for('.user'))


# 用户管理
@admin.route('/user', methods=['GET', 'POST'])
@admin_required
def user():
    page = request.args.get('page', 1, type=int)
    keyword = request.form.get('keyword', None, type=int)
    value = request.form.get('value', None)
    query = User.query.order_by(User.updated_at.desc())
    if keyword and value:
        if keyword == 1:
            query = Seeker.query.filter(Seeker.name.contains(value))
        elif keyword == 2:
            query = Company.query.filter(Company.name.contains(value))
        elif keyword == 3:
            query = User.query.filter(User.email.contains(value))
        page = 1

    pagination = query.paginate(
        per_page=10,
        page=page,
        error_out=False
    )
    return render_template('admin/user.html', pagination=pagination)


@admin.route('/user/add', methods=['GET', 'POST'])
@admin_required
def user_add():
    form = UserForm()
    if form.validate_on_submit():
        form.save()
        flash('添加成功', 'success')
        return redirect(url_for('admin.user'))
    return render_template('admin/form.html', title='添加用户', form=form)


@admin.route('/user/update/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def user_update(user_id):
    user = User.query.get_or_404(user_id)
    form = UserUpdateForm(obj=user)
    if form.validate_on_submit():
        form.save(user)
        flash('修改成功', 'success')
        return redirect(url_for('admin.user'))
    return render_template('admin/form.html', title='修改用户', form=form)


@admin.route('/user/delete/<int:user_id>')
@admin_required
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    UserForm.delete(user)
    flash('删除成功', 'success')
    return redirect(url_for('admin.user'))


# 职位管理
@admin.route('/job')
@admin_required
def job():
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.order_by(Job.updated_at.desc()).paginate(
        per_page=10,
        page=page,
        error_out=False
    )
    return render_template('admin/job.html', pagination=pagination)


@admin.route('/job/delete/<int:job_id>')
@admin_required
def job_delete(job_id):
    job = Job.query.get_or_404(job_id)
    BaseForm.delete(job)
    flash('删除成功', 'success')
    return redirect(url_for('admin.job'))


# 标签管理
@admin.route('/tag')
@admin_required
def tag():
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.order_by(Tag.updated_at.desc()).paginate(
        per_page=10,
        page=page,
        error_out=False
    )
    return render_template('admin/tag.html', pagination=pagination)


@admin.route('/tag/delete/<int:tag_id>')
@admin_required
def tag_delete(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    BaseForm.delete(tag)
    flash('删除成功', 'success')
    return redirect(url_for('admin.tag'))


@admin.route('/tag/add', methods=['GET', 'POST'])
@admin_required
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        form.save_self()
        flash('添加成功', 'success')
        return redirect(url_for('admin.tag'))
    return render_template('admin/form.html', title='添加标签', form=form)
