# # app.py — Streamlit form for Interview-Prep Agent
import streamlit as st
import requests, base64, mimetypes, os

WEBHOOK_URL = "https://hadasbenmoshe.app.n8n.cloud/webhook/interview-prep"

st.set_page_config(page_title="Interview-Prep AI", page_icon=":rocket:")

st.markdown(
    """
    <h1 style='text-align:center;
               color:#2BB0B6;
               font-size:2.6rem;
               text-shadow: 1px 1px 2px rgba(0,0,0,0.25);'>
        🤖 AI Interview-Prep Agent
    </h1>
    <h4 style='text-align:center;
               color:#505050;
               margin-top:-0.6rem;
               font-weight:500;'>
        Resume ➜ Insights ➜ Perfect Interview 🚀
    </h4>
    """,
    unsafe_allow_html=True
)

st.info(
    "Your AI agent for interview prep – upload your resume, add links, and receive smart insights & interview questions straight to your inbox."
)

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