# routes/dashboard.py

from flask import Blueprint, render_template, session, redirect, url_for

# Buat blueprint dengan nama 'dashboard'
dashboard_bp = Blueprint('dashboard', __name__)

# Endpoint: 'dashboard.dashboard'
@dashboard_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', user=session['username'])