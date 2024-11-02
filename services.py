# services.py

import os
from pdf2docx import Converter
from docx2pdf import convert
import messages

def convert_pdf_to_docx(input_path, output_folder):
    """Konversi file PDF ke DOCX."""
    if not input_path.endswith('.pdf'):
        raise ValueError(messages.INVALID_FORMAT_OR_TYPE)
    
    output_filename = os.path.basename(input_path).rsplit('.', 1)[0] + '.docx'
    output_path = os.path.join(output_folder, output_filename)

    cv = Converter(input_path)
    cv.convert(output_path)
    cv.close()
    
    return output_path

def convert_docx_to_pdf(input_path, output_folder):
    """Konversi file DOCX ke PDF."""
    if not input_path.endswith('.docx'):
        raise ValueError(messages.INVALID_FORMAT_OR_TYPE)
    
    output_filename = os.path.basename(input_path).rsplit('.', 1)[0] + '.pdf'
    output_path = os.path.join(output_folder, output_filename)

    convert(input_path, output_path)
    
    return output_path