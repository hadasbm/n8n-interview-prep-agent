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

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    print(f"✅ הניתוח נשלח למייל: {email}")
else:
    print("❌ שגיאה בשליחה")