# 🎯 Interview Prep Automation

An intelligent automation system that analyzes resumes and generates comprehensive interview preparation documents using AI.

## ✨ Features

- 📄 **Resume Analysis**: Extract and analyze text from PDF/DOCX files
- 🤖 **AI-Powered Insights**: Generate detailed feedback using Gemini AI
- 📝 **Interview Questions**: Create 15 technical interview questions with answers
- 💼 **Job Matching**: Analyze resume compatibility with job descriptions
- 📧 **Email Delivery**: Automatically send results via email
- 📋 **Word Document**: Export everything to a formatted DOCX file

## 🏗️ Architecture

- **n8n**: Workflow automation platform
- **Flask API**: Resume processing and document generation
- **Gemini AI**: Content analysis and generation
- **Docker**: Containerized deployment

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/interview-prep-agent
   cd interview-prep-agent
   ```

2. **Configure the webhook URL**
   
   Edit `send_to_n8n.py` and update the webhook URL:
   ```python
   WEBHOOK_URL = "http://localhost:5678/webhook/YOUR-WEBHOOK-ID"  # Replace with your webhook
   ```

3. **Start the services**
   ```bash
   docker compose build
   docker compose up -d
   ```

4. **Import the n8n workflow**
   - Open n8n at `http://localhost:5678`
   - Import the `workflow.json` file
   - Configure your Gemini API key and email credentials

5. **Run the automation**
   ```bash
   python send_to_n8n.py
   ```

### Stopping the services
```bash
docker compose down
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key_here
N8N_WEBHOOK_URL=http://localhost:5678/webhook/your-webhook-id
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

### Email Setup

1. **Gmail**: Use an App Password (not your regular password)
2. **Other providers**: Update SMTP settings in the n8n workflow

### API Endpoints

The Flask API provides these endpoints:

- `POST /extract_resume`: Extract text from PDF/DOCX files
- `POST /generate_docx`: Generate Word documents from text

## 📋 Usage

### Input Requirements

- **Resume file**: PDF or DOCX format
- **Job link** (optional): URL to job posting
- **Company link** (optional): Company website
- **LinkedIn profile** (optional): Your LinkedIn URL

### Sample Request

The `send_to_n8n.py` script handles the file upload and processing:

```python
python send_to_n8n.py
```

Follow the prompts to:
1. Select your resume file
2. Enter job details (optional)
3. Provide email address for results

### Output

You'll receive an email with:
- 📊 Detailed resume analysis
- 💡 Improvement recommendations  
- ❓ 15 technical interview questions with answers
- 🎯 Job matching insights (if job link provided)
- 📎 Complete analysis as a Word document attachment

## 🐳 Docker Services

### Services Overview

- **n8n**: Workflow automation (`localhost:5678`)
- **resume-api**: Flask API for file processing (`localhost:5001`)

### Container Management

```bash
# Build and start
docker compose build
docker compose up -d

# View logs
docker compose logs -f

# Restart specific service
docker compose restart resume-api

# Stop all services
docker compose down
```

## 🛠️ Development

### Project Structure

```
interview-prep-automation/
├── README.md
├── docker-compose.yml
├── Dockerfile                    # n8n container
├── Dockerfile.resume-api        # Flask API container
├── send_to_n8n.py              # Client script
├── app.py                       # Flask application
├── workflow.json                # n8n workflow export
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment template
```

### Local Development

1. **Run Flask API locally**:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

2. **Access n8n**: `http://localhost:5678`
3. **API docs**: Flask API runs on `http://localhost:5001`

## 🔍 Troubleshooting

### Common Issues

**1. Webhook not working**
- Check the webhook URL in `send_to_n8n.py`
- Ensure n8n workflow is activated
- Verify webhook ID matches

**2. Email not sending**
- Check SMTP credentials
- Use App Passwords for Gmail
- Verify email configuration in n8n

**3. File processing errors**
- Ensure resume is in PDF or DOCX format
- Check file size limits
- Verify file is not corrupted

**4. Docker issues**
- Check if ports 5678 and 5001 are available
- Run `docker compose logs` to see error details
- Restart with `docker compose down && docker compose up -d`

### Logs

```bash
# View all logs
docker compose logs

# View specific service logs
docker compose logs resume-api
docker compose logs n8n
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [n8n](https://n8n.io/) for workflow automation
- [Google Gemini](https://ai.google.dev/) for AI capabilities
- [python-docx](https://python-docx.readthedocs.io/) for document generation

**Made with ❤️ for job seekers everywhere**