import requests
import base64

email = "<YOUR-EMAIL>"

with open(r"<YOUR-PATH-TO-CV>", 'rb') as file:
    file_content = file.read()
    encoded_file = base64.b64encode(file_content).decode('utf-8')

url = "https://hadasbenmoshe.app.n8n.cloud/webhook/interview-prep" #dont change!
data = {
    'email': email,
    'jobLink': '<PATH-TO-JOB>',
    'companyLink': '<PATH-TO-COMPANY>',
    'linkedinProfile': '<PATH-TO-LINKEDIN-PROFILE>',
    'resume': encoded_file,
    'resumeFilename': '<CV-FILE-NAME>', #(optional)
    'resumeMimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  #for PDF use: application/pdf
}

try:
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    print(f"✅ הניתוח נשלח למייל: {email}")
except requests.HTTPError as e:
    print("❌ שגיאה:", resp.status_code, resp.text)