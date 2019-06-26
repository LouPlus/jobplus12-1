from flask import Blueprint, render_template, request, flash, redirect, url_for

from jobplus.decorators import company_required
from jobplus.forms import CompanyProfileForm, CompanyLogoForm
from jobplus.models import Company

company = Blueprint('company', __name__, url_prefix='/company')


@company.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    query = Company.query.order_by(Company.updated_at.desc())
    keyword = request.args.get('keyword') or request.form.get('keyword')
    if isinstance(keyword, str):
        keyword = keyword.strip()
    if keyword:
        query = Company.query.filter(Company.name.contains(keyword)).order_by(Company.updated_at.desc())
    pagination = query.paginate(
        page=page,
        per_page=12,
        error_out=False
    )
    return render_template('company/index_company.html', pagination=pagination)


@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/detail.html', company=company)


@company.route('/profile/<int:company_id>', methods=['GET', 'POST'])
@company_required
def profile(company_id):
    company = Company.query.get_or_404(company_id)
    form = CompanyProfileForm(obj=company)
    if form.validate_on_submit():
        form.save(company)
        flash('保存成功', 'success')
        return redirect(url_for('user.index'))
    return render_template('company/edit.html', form=form)


@company.route('/logo/<int:company_id>', methods=['GET', 'POST'])
@company_required
def logo(company_id):
    company = Company.query.get_or_404(company_id)
    form = CompanyLogoForm()
    if form.validate_on_submit():
        form.save(company)
        flash('保存成功', 'success')
        return redirect(url_for('user.index'))
    return render_template('company/logo.html', form=form)
