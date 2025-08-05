from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    """Restrict access to admin users only"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page", "danger")
            return redirect(url_for('auth.login'))
        if current_user.role != 'admin':
            flash("Admin access required", "danger")
            return redirect(url_for('student.dashboard'))
        return f(*args, **kwargs)
    return decorated_function