from flask import Blueprint, render_template, request, make_response
from jinja2 import Template
import pdfkit
from flask import Response


calculate_bp = Blueprint('calculate', __name__, url_prefix='/calculate')

@calculate_bp.route('/', methods=['POST'])
def calculate():
    total = float(request.form['total_laba'])
    porsi_a = float(request.form['porsi_a'])
    porsi_b = float(request.form['porsi_b'])

    bagian_a = total * (porsi_a / 100)
    bagian_b = total * (porsi_b / 100)

    return render_template(
        'hasil_pembagian.html',
        total=total,
        porsi_a=porsi_a,
        porsi_b=porsi_b,
        bagian_a=bagian_a,
        bagian_b=bagian_b
    )


@calculate_bp.route('/download_pdf', methods=['POST'])
def download_pdf():
    total = float(request.form['total'])
    porsi_a = float(request.form['porsi_a'])
    porsi_b = float(request.form['porsi_b'])
    bagian_a = float(request.form['bagian_a'])
    bagian_b = float(request.form['bagian_b'])

    html = render_template(
        'hasil_pembagian_pdf.html',
        total=total,
        porsi_a=porsi_a,
        porsi_b=porsi_b,
        bagian_a=bagian_a,
        bagian_b=bagian_b
    )

    pdf = pdfkit.from_string(html, False)

    return Response(pdf, mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment; filename=laporan_pembagian.pdf'})

