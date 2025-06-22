FROM n8nio/n8n

USER root

RUN apk update && apk add --no-cache python3 py3-pip

RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir PyPDF2 python-docx

ENV PATH="/opt/venv/bin:$PATH"

USER node