# Snap to the version with security fixes
FROM n8nio/n8n:1.106.3-alpine

USER root

RUN apk update && apk add --no-cache python3 py3-pip

RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir PyPDF2 python-docx

ENV PATH="/opt/venv/bin:$PATH"

# Exclude specific n8n nodes
ENV N8N_NODES_EXCLUDE="n8n-nodes-base.executeCommand"

USER node