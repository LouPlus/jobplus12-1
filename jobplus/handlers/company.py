from flask import Blueprint, render_template, request
from jobplus.models import Company

company = Blueprint('company', __name__, url_prefix='/company')


@company.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Company.query.paginate(
        page=page,
        per_page=12,
        error_out=False
    )
    return render_template('company/index_company.html', pagination=pagination)


@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/detail.html', company=company)
