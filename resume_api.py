from flask import Flask, request, jsonify, send_file  
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import tempfile
import re

app = Flask(__name__)

def set_rtl_paragraph(paragraph):
    """הגדרת כיווניות מימין לשמאל לפסקה"""
    pPr = paragraph._element.get_or_add_pPr()
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    pPr.append(bidi)

def is_hebrew_text(text):
    """בדיקה אם הטקסט מכיל עברית"""
    hebrew_chars = re.findall(r'[\u0590-\u05FF]', text)
    return len(hebrew_chars) > 0

def add_styled_paragraph(doc, text, style_type='normal'):
    """הוספת פסקה עם עיצוב מתאים"""
    para = doc.add_paragraph()
    
    # הגדרת עיצוב לפי סוג
    if style_type == 'heading':
        run = para.add_run(text)
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 51, 102)  # כחול כהה
    elif style_type == 'subheading':
        run = para.add_run(text)
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 51, 51)  # אפור כהה
    else:
        run = para.add_run(text)
        run.font.size = Pt(11)
    
    # הגדרת גופן
    run.font.name = 'Calibri'
    r = run._element
    r.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
    
    # הגדרת כיווניות
    if is_hebrew_text(text):
        para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        set_rtl_paragraph(para)
    else:
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    return para

def parse_markdown_to_docx(doc, text):
    """המרת טקסט מעוצב לפורמט Word"""
    lines = text.split('\n')
    current_list_items = []
    
    for line in lines:
        line = line.strip()
        if not line:
            # אם יש רשימה פתוחה, סגור אותה
            if current_list_items:
                add_list_to_doc(doc, current_list_items)
                current_list_items = []
            continue
        
        # זיהוי כותרות
        if line.startswith('###'):
            if current_list_items:
                add_list_to_doc(doc, current_list_items)
                current_list_items = []
            clean_text = line.replace('###', '').strip()
            add_styled_paragraph(doc, clean_text, 'heading')
            
        elif line.startswith('##'):
            if current_list_items:
                add_list_to_doc(doc, current_list_items)
                current_list_items = []
            clean_text = line.replace('##', '').strip()
            add_styled_paragraph(doc, clean_text, 'subheading')
            
        # זיהוי רשימות ממוספרות
        elif re.match(r'^\d+\.', line):
            current_list_items.append(('numbered', line))
            
        # זיהוי רשימות עם נקודות
        elif line.startswith('- ') or line.startswith('• '):
            current_list_items.append(('bullet', line))
            
        # טקסט רגיל
        else:
            if current_list_items:
                add_list_to_doc(doc, current_list_items)
                current_list_items = []
            
            # ניקוי תווים מיוחדים
            clean_text = (line.replace('**', '')
                            .replace('***', '')
                            .replace('__', '')
                            .replace('```', '')
                            .replace('\u200E', ''))
            
            if clean_text:
                add_styled_paragraph(doc, clean_text)
    
    # סגירת רשימה אחרונה אם קיימת
    if current_list_items:
        add_list_to_doc(doc, current_list_items)

def add_list_to_doc(doc, list_items):
    """הוספת רשימה למסמך"""
    for item_type, item_text in list_items:
        # ניקוי הטקסט
        if item_type == 'numbered':
            clean_text = re.sub(r'^\d+\.\s*', '', item_text)
        else:
            clean_text = item_text.replace('- ', '').replace('• ', '')
        
        # יצירת פסקה עם רשימה
        para = doc.add_paragraph()
        
        # הוספת מספור או נקודה
        if item_type == 'numbered':
            para.style = 'List Number'
        else:
            para.style = 'List Bullet'
        
        run = para.add_run(clean_text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        
        # הגדרת כיווניות
        if is_hebrew_text(clean_text):
            para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            set_rtl_paragraph(para)
        else:
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT

@app.route('/generate_docx', methods=['POST'])
def generate_docx():
    data = request.json
    text = data.get("text", "").strip()
    
    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    try:
        doc = Document()
        
        # הגדרת כותרת ראשית
        title = doc.add_heading('📋 הכנה לראיון עבודה - Gemini AI', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_rtl_paragraph(title)
        
        # הוספת קו מפריד
        doc.add_paragraph('_' * 50).alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # עיבוד הטקסט
        parse_markdown_to_docx(doc, text)
        
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