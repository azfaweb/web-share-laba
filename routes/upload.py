from flask import Blueprint, render_template, request, redirect, flash
import os
from werkzeug.utils import secure_filename
from utils.parser import parse_laporan_sap
import json
import csv
from datetime import datetime
from flask import request
from flask import session
import sqlite3



upload_bp = Blueprint('upload', __name__, url_prefix='/upload')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                df = parse_laporan_sap(filepath)
                
                # Simpan nama kolom
                kolom_now = 'Total of Reporting Period'
                kolom_prev = 'Total of the Comparison Period'
                kolom_diff = 'Absolute Difference'
                
                total = df[kolom_now].sum()
                simpan_audit_log(filename, total, request.remote_addr)


                # Format ribuan hanya untuk tampilan
                df[kolom_now] = df[kolom_now].apply(lambda x: f"{x:,.0f}")
                df[kolom_prev] = df[kolom_prev].apply(lambda x: f"{x:,.0f}")
                df[kolom_diff] = df[kolom_diff].apply(lambda x: f"{x:,.0f}")

                # Data untuk chart (pakai 10 akun teratas)
                chart_data = df.head(10)[['Text for B/S P&L Item', kolom_now]].copy()
                chart_data[kolom_now] = chart_data[kolom_now].str.replace(',', '').astype(float)
                labels = chart_data['Text for B/S P&L Item'].tolist()
                values = chart_data[kolom_now].tolist()
                colors = ['rgba(75, 192, 192, 0.7)' if v >= 0 else 'rgba(255, 99, 132, 0.7)' for v in values]
                # Warna bisa digenerate dinamis, pakai warna pie default
                pie_colors = [
                    'rgba(255, 99, 132, 0.7)', 'rgba(54, 162, 235, 0.7)', 'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)', 'rgba(255, 159, 64, 0.7)',
                    'rgba(231, 233, 237, 0.7)', 'rgba(100, 149, 237, 0.7)', 'rgba(220, 20, 60, 0.7)', 'rgba(46, 139, 87, 0.7)'
                    ]



                # Tampilkan ke HTML
                table_html = df.to_html(classes='table table-striped table-bordered', index=False, escape=False)
                return render_template(
                    'result.html',
                    table=table_html,
                    total=total,
                    labels=json.dumps(labels),  # convert Python list to JS array
                    values=json.dumps(values),
                    colors=json.dumps(colors),
                    pie_colors=json.dumps(pie_colors)

                    )


            except Exception as e:
                return f"Gagal parsing file: {str(e)}"

        flash("Hanya menerima file .xlsx")
        return redirect(request.url)

    return render_template('upload.html')

from flask import send_file
import io
import pandas as pd

@upload_bp.route('/download_excel', methods=['POST'])
def download_excel():
    # Ambil data dari form tersembunyi
    df_data = request.form.get('df_data')
    if not df_data:
        return "Data tidak tersedia", 400

    # Ubah kembali dari JSON string ke DataFrame
    df = pd.read_json(df_data)

    # Simpan ke Excel di memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Laporan SAP')

    output.seek(0)
    return send_file(output,
                     download_name="laporan_sap.xlsx",
                     as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def simpan_audit_log(filename, total_laba, ip_address):
    log_path = os.path.join('logs', 'audit_log.csv')
    log_data = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename, total_laba, ip_address]

    header = ['timestamp', 'filename', 'total_laba', 'ip_address']
    file_exists = os.path.isfile(log_path)

    with open(log_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(log_data)

@upload_bp.route('/logs')
def view_logs():
    if 'role' not in session or session['role'] != 'admin':
        return "Akses ditolak. Hanya admin yang boleh melihat log."

    conn = sqlite3.connect('share_laba.db')
    c = conn.cursor()
    c.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC")
    logs = c.fetchall()
    conn.close()

    return render_template('audit_log.html', logs=logs)
