from flask import session, flash, redirect, url_for
from functools import wraps

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('user_logged_in') or session.get('user_role') != 'admin':
            flash("Akses ditolak! Silahkan login sebagai admin.", "danger")
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return wrap

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('user_logged_in'):
            flash("Silahkan login terlebih dahulu.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap