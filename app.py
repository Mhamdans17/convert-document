from flask import Flask, request, render_template, jsonify, send_file
import os
import messages  # Impor pesan dari file messages.py
from services import convert_pdf_to_docx, convert_docx_to_pdf  # Impor fungsi konversi

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({"error": messages.NO_FILE_UPLOADED}), 400

    uploaded_file = request.files['file']
    conversion_type = request.form['conversion_type']

    if uploaded_file.filename == '':
        return jsonify({"error": messages.FILE_NOT_FOUND}), 400

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(input_path)

    try:
        if conversion_type == 'pdf_to_docx':
            output_path = convert_pdf_to_docx(input_path, app.config['UPLOAD_FOLDER'])
        elif conversion_type == 'docx_to_pdf':
            output_path = convert_docx_to_pdf(input_path, app.config['UPLOAD_FOLDER'])
        else:
            return jsonify({"error": messages.INVALID_FORMAT_OR_TYPE}), 400

        return send_file(output_path, as_attachment=True)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": messages.CONVERSION_ERROR}), 500

if __name__ == '__main__':
    app.run(debug=True)
