from flask import abort
from functools import wraps

from flask_login import current_user

from jobplus.models import User


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not isinstance(role, list):
                if not current_user.is_authenticated or current_user.role != role:
                    abort(404)
            else:
                if not current_user.is_authenticated or current_user.role not in role:
                    abort(404)
            return func(*args, **kwargs)

        return wrapper

    return decorator


company_required = role_required(User.ROLE_COMPANY)
seeker_required = role_required(User.ROLE_SEEKER)
admin_required = role_required(User.ROLE_ADMIN)

company_admin_required = role_required([User.ROLE_COMPANY, User.ROLE_ADMIN])
