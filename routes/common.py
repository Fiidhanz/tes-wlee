from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import SosmedData, TrendsData # Import model jika perlu

common_bp = Blueprint('common', __name__)

@common_bp.route('/')
def landing():
    return render_template('index.html')

@common_bp.route('/logout')
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for('common.landing'))