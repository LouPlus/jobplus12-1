from flask import render_template, Blueprint, request
from jobplus.models import Job

job = Blueprint('job', __name__, url_prefix='/job')

@job.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=12,
        error_out=False
    )
    return render_template('job/index.html', pagination=pagination)