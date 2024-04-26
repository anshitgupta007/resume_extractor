from django.http import HttpResponse
import zipfile
import os
import pdfplumber
import re
import pandas as pd
import io
from docx import Document
from django.shortcuts import render

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_REGEX = re.compile(r'\b\d{3}[-.\s]?\d{2,3}[-.\s]?\d{4}\b|\b\d{5}\s\d{5}\b')

def extract_information_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages)

        email = EMAIL_REGEX.findall(text)
        phone = PHONE_REGEX.findall(text)

        return {
            "email": email[0] if email else None,
            "phone": phone[0] if phone else None,
            "text": text
        }

def extract_information_from_docx(file):
    doc = Document(file)
    text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)

    email = EMAIL_REGEX.findall(text)
    phone = PHONE_REGEX.findall(text)

    return {
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "text": text
    }

def upload_zip(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('zip_file')
        if uploaded_file:
            # Open the uploaded ZIP file
            zip_file = zipfile.ZipFile(uploaded_file, 'r')
            # Processing and generating Excel in memory
            data = []
            for file_info in zip_file.infolist():
                with zip_file.open(file_info) as file:
                    file_name = file_info.filename
                    file_ext = os.path.splitext(file_name)[1]
                    if file_ext == '.pdf':
                        extracted_info = extract_information_from_pdf(file)
                    elif file_ext == '.docx':
                        extracted_info = extract_information_from_docx(file)
                    else:
                        continue
                    data.append(extracted_info)
            zip_file.close()
            df = pd.DataFrame(data)
            # Generate Excel file in memory
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            # Provide Excel file as downloadable response
            response = HttpResponse(excel_buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=extracted_info.xlsx'
            return response
    return render(request, 'upload_zip.html')
