# # app.py — Streamlit form for Interview-Prep Agent
import streamlit as st
import requests, base64, mimetypes, os

WEBHOOK_URL = "https://hadasbenmoshe.app.n8n.cloud/webhook/interview-prep"

st.set_page_config(page_title="Interview-Prep AI", page_icon=":rocket:")

st.markdown("""
<style>
div.stButton > button:first-child {
    background-color:#4F8BF9; color:white; border-radius:8px; height:3em;
}
div.stButton > button:hover { background-color:#3c6dd8; }
</style>

<h1 style='text-align:center; color:#4F8BF9;'>
  🤖 AI Interview-Prep Agent
</h1>
""", unsafe_allow_html=True)

email  = st.text_input("📧 Email")
job    = st.text_input("🔗 Job Link")
comp   = st.text_input("🏢 Company Link")
lnkdin = st.text_input("💼 LinkedIn Profile (optional)")
file   = st.file_uploader("📄 Upload resume (PDF or DOCX)", type=["pdf","docx"])

if st.button("🚀 Analyze"):
    if not (file and email and job and comp):
        st.warning("Please fill in the required fields 👆")
    else:
        with st.spinner("⌛ Sending… please wait"):
            data = base64.b64encode(file.read()).decode()
            mime = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
            payload = {
                "email": email, "jobLink": job, "companyLink": comp,
                "linkedinProfile": lnkdin, "resume": data,
                "resumeFilename": file.name, "resumeMimeType": mime
            }
            try:
                r = requests.post(WEBHOOK_URL, json=payload, timeout=120)
                if r.status_code == 200:
                    st.success("✅ Sent! Check your inbox 📬")
                else:
                    st.error(f"❌ Error {r.status_code}: {r.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")