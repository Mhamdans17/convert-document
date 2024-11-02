from flask import Flask, request, render_template, send_file
from pdf2docx import Converter
from docx2pdf import convert
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Membuat folder untuk menyimpan file yang diunggah
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return "Tidak ada file yang diunggah.", 400

    uploaded_file = request.files['file']
    conversion_type = request.form['conversion_type']

    if uploaded_file.filename == '':
        return "File tidak ditemukan.", 400

    # Simpan file yang diunggah
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(input_path)

    if conversion_type == 'pdf_to_docx' and input_path.endswith('.pdf'):
        # Konversi PDF ke DOCX
        output_filename = uploaded_file.filename.rsplit('.', 1)[0] + '.docx'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()
    elif conversion_type == 'docx_to_pdf' and input_path.endswith('.docx'):
        # Konversi DOCX ke PDF
        output_filename = uploaded_file.filename.rsplit('.', 1)[0] + '.pdf'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        convert(input_path, output_path)
    else:
        return "Format file atau tipe konversi tidak sesuai.", 400

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
