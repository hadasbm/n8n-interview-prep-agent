from flask import Flask, request, jsonify, send_file  
import base64
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
import tempfile
import os
import re

app = Flask(__name__)

def set_rtl_paragraph(paragraph):
    """הגדרת כיווניות מימין לשמאל לפסקה - גישה פשוטה יותר"""
    try:
        # הגדרת RTL ברמת הפסקה
        pPr = paragraph._element.get_or_add_pPr()
        
        # יצירת אלמנט bidi (bidirectional text)
        bidi = OxmlElement('w:bidi')
        pPr.append(bidi)
        
        # הגדרת כיוון הטקסט
        jc = OxmlElement('w:jc')
        jc.set(qn('w:val'), 'right')
        pPr.append(jc)
        
    except Exception as e:
        print(f"RTL error: {e}")

# פונקציות עזר מוסרות - לא נדרשות יותר

@app.route('/', methods=['GET'])
def home():
    return "📋 Resume Agent API is up and running!", 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

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
        "resumeFileName": data.get("resumeFileName")
    })

@app.route('/generate_docx', methods=['POST'])
def generate_docx():
    data = request.json
    text = data.get("text", "").strip()
    
    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    try:
        doc = Document()
        
        # כותרת ראשית
        title = doc.add_heading('📋 Interview Preparation - Gemini AI', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in title.runs:
            run.font.name = 'Calibri'
            run.font.color.rgb = RGBColor(0, 51, 102)
        
        # קו מפריד
        separator = doc.add_paragraph('═' * 60)
        separator.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # ניקוי יסודי של תווים לא רצויים
        cleaned_text = (text.replace('***', '')
                           .replace('**', '')
                           .replace('###', '')
                           .replace('##', '')
                           .replace('#', '')
                           .replace('```', '')
                           .replace('__', '')
                           .replace('*', '')
                           .replace('---', '')
                           .replace('–', '-')
                           .replace('\r', '')
                           .replace('\u200E', ''))
        
        # חלוקה לפסקאות ועיצוב פשוט וברור
        sections = cleaned_text.split('\n\n')
        for section in sections:
            if section.strip():
                lines = section.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        # הסרת מספרים מתחילת השורה
                        clean_line = re.sub(r'^\d+\.\s*', '', line)
                        
                        # זיהוי כותרות משופר
                        is_heading = False
                        heading_keywords = ['ניתוח', 'התאמה', 'החברה', 'שאלות', 'משפטי מפתח', 'Akamai', 'קורות החיים']
                        
                        # בדיקה אם זה כותרת (קצר ומכיל מילת מפתח)
                        if (len(clean_line.split()) <= 8 and 
                            any(keyword in clean_line for keyword in heading_keywords)):
                            is_heading = True
                        
                        # בדיקה נוספת לכותרות שמתחילות בביטויים מסוימים
                        if any(clean_line.startswith(prefix) for prefix in ['ניתוח', 'התאמה', 'שאלות', 'משפטי']):
                            is_heading = True
                        
                        paragraph = doc.add_paragraph()
                        run = paragraph.add_run(clean_line)
                        
                        # עיצוב מובדל לכותרות וטקסט רגיל
                        if is_heading:
                            run.font.bold = True
                            run.font.size = Pt(15)  # גדול יותר לכותרות
                            run.font.color.rgb = RGBColor(0, 51, 102)  # כחול כהה
                        else:
                            run.font.bold = False
                            run.font.size = Pt(11)  # טקסט רגיל
                        
                        # גופן אחיד
                        run.font.name = 'Calibri'
                        
                        # הגדרת יישור לימין וRTL
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                        set_rtl_paragraph(paragraph)
        
        # יצירת קובץ זמני
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        doc.save(temp.name)
        
        return send_file(temp.name,
                         as_attachment=True,
                         download_name='Interview_Preparation.docx',
                         mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                         
    except Exception as e:
        return jsonify({"error": f"Failed to generate DOCX: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)