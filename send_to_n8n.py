import requests
import base64
import mimetypes

email = "<YOUR-EMAIL>"

cv_path = r"<YOUR-PATH-TO-CV>"

with open(cv_path, "rb") as file:
    encoded_file = base64.b64encode(file.read()).decode()

url = "https://hadasbenmoshe.app.n8n.cloud/webhook/interview-prep" #dont change!
# Automatically determine MIME type from file extension
resume_mime_type = mimetypes.guess_type(cv_path)[0] or "application/octet-stream"

payload = {
    'email': email,
    'jobLink': '<PATH-TO-JOB>',
    'companyLink': '<PATH-TO-COMPANY>',
    'linkedinProfile': '<PATH-TO-LINKEDIN-PROFILE>',
    'resume': encoded_file,
    'resumeFilename': '<CV-FILE-NAME>', #(optional)
    'resumeMimeType': resume_mime_type  # automatically determined from file extension
}

try:
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    print(f"✅ הניתוח נשלח למייל: {email}")
except requests.HTTPError as e:
    print("❌ שגיאה:", resp.status_code, resp.text)