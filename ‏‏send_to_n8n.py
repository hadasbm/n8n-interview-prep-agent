import requests
import base64

email = "hadas414@gmail.com"

with open(r"C:\Users\hagit\Downloads\Hadas_Ben_Moshe_CV.docx", 'rb') as file:
    file_content = file.read()
    encoded_file = base64.b64encode(file_content).decode('utf-8')

url = "http://localhost:5678/webhook/interview-prep"
data = {
    'email': email,
    'jobLink': 'https://jobs.akamai.com/en/sites/CX_1/job/621?keyword=devops&mode=location',
    'companyLink': 'https://www.akamai.com/company',
    'linkedinProfile': 'https://www.linkedin.com/in/hadas-ben-moshe',
    'resume': encoded_file,
    'resumeFilename': 'Hadas_Ben_Moshe_CV.docx',
    'resumeMimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    print(f"✅ הניתוח נשלח למייל: {email}")
else:
    print("❌ שגיאה בשליחה")