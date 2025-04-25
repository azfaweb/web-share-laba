from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import sqlite3

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('share_laba.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = user[1]
            session['role'] = user[3]
            flash(f"Selamat datang, {user[1]}!", "success")
            return redirect(url_for('upload.upload'))  # arahkan ke halaman utama
        else:
            flash("Login gagal. Periksa username/password.", "danger")

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
