from flask import Flask, request, jsonify, send_file  
import base64
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document
import tempfile 

app = Flask(__name__)

@app.route('/extract_resume', methods=['POST'])
def extract_resume():
    data = request.json
    if not data or 'resume' not in data:
        return jsonify({"error": "Missing resume field"}), 400

    resume_b64 = data['resume']
    mime_type = data.get('resumeMimeType', '')
    try:
        file_bytes = base64.b64decode(resume_b64)
    except Exception as e:
        return jsonify({"error": f"Invalid base64: {str(e)}"}), 400

    try:
        if mime_type == "application/pdf":
            reader = PdfReader(BytesIO(file_bytes))
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        elif mime_type in [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ]:
            doc = Document(BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            return jsonify({"error": f"Unsupported MIME type: {mime_type}"}), 415
    except Exception as e:
        return jsonify({"error": f"Error reading file: {str(e)}"}), 500

    return jsonify({
        "resumeText": text,
        "length": len(text),
        "jobLink": data.get("jobLink"),
        "companyLink": data.get("companyLink"),
        "linkedinProfile": data.get("linkedinProfile"),
        "resumeFileName": data.get("resumeFileName")  # אם נדרש בהמשך
    })

@app.route('/generate_docx', methods=['POST'])
def generate_docx():
    data = request.json
    text = data.get("text", "").strip()
    
    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    try:
        doc = Document()

        heading = doc.add_heading('📋 Interview Preparation - Gemini AI', 0)
        heading.alignment = 2  # RTL alignment
        
        cleaned_text = text.replace('***', '').replace('###', '').replace('**', '')
        
        for section in cleaned_text.split('\n\n'):
            if section.strip():
                paragraph = doc.add_paragraph(section.strip())
                paragraph.alignment = 2  # RTL alignment
                for run in paragraph.runs:
                    run.font.name = 'Arial'
                    
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        doc.save(temp.name)
        
        return send_file(temp.name,
                         as_attachment=True,
                         download_name='Interview_Prep.docx',
                         mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                         
    except Exception as e:
        return jsonify({"error": f"Failed to generate DOCX: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
