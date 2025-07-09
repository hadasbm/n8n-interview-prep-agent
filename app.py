# app.py — Streamlit form for Interview-Prep Agent
import streamlit as st
import requests, base64, mimetypes, os

st.set_page_config(page_title="Interview-Prep AI", page_icon="🤖")
st.title("🤖 AI Interview-Prep Agent (n8n Cloud)")

email  = st.text_input("📧 Email")
job    = st.text_input("🔗 Job Link")
comp   = st.text_input("🏢 Company Link")
lnkdin = st.text_input("💼 LinkedIn Profile (optional)")
file   = st.file_uploader("📄 Upload resume (PDF or DOCX)", type=["pdf", "docx"])

if st.button("🚀 Analyze"):
    if not (file and email and job and comp):
        st.warning("Please fill in Email, Job Link, Company Link and upload a file.")
    else:
        data      = base64.b64encode(file.read()).decode()
        mime_type = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
        payload   = {
            "email":            email,
            "jobLink":          job,
            "companyLink":      comp,
            "linkedinProfile":  lnkdin,
            "resume":           data,
            "resumeFilename":   file.name,
            "resumeMimeType":   mime_type,
        }
        try:
            r = requests.post(
                "https://hadasbenmoshe.app.n8n.cloud/webhook/interview-prep",
                json=payload,
                timeout=120,
            )
            if r.status_code == 200:
                st.success("✅ Sent! Check your inbox.")
            else:
                st.error(f"❌ Error {r.status_code}: {r.text}")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")