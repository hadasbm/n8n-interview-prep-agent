from flask import Flask, request, jsonify, send_file
from docx import Document
from docx.shared import Pt
import tempfile

app = Flask(__name__)

@app.route('/generate_docx', methods=['POST'])
def generate_docx():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    try:
        doc = Document()

        # כותרת ראשית
        heading = doc.add_heading('📋 Interview Preparation - Gemini AI', 0)
        heading.alignment = 2  # יישור לימין

        # חלוקה לפי פסקאות קיימות
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        for para in paragraphs:
            # פסקאות שהן כותרות נזהה לפי סימן ":" או אורך קצר
            if ":" in para or len(para.split()) <= 4:
                run = doc.add_paragraph().add_run(para)
                run.bold = True
                run.font.name = 'Arial'
                run.font.size = Pt(12)
            else:
                paragraph = doc.add_paragraph(para)
                paragraph.alignment = 2
                for run in paragraph.runs:
                    run.font.name = 'Arial'
                    run.font.size = Pt(11)

        # שמירת הקובץ הזמני
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        doc.save(temp.name)

        return send_file(
            temp.name,
            as_attachment=True,
            download_name='Interview_Prep.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        return jsonify({"error": f"Failed to generate DOCX: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)