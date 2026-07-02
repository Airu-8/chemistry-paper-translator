# Chemistry Paper Translator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A full-stack web application for translating chemistry research papers from PDF with context-aware translation.

## 🔍 Features

- **PDF Upload**: Upload chemistry research papers in PDF format
- **Context-Aware Translation**: AI-powered translation that understands chemical terminology
- **Preserve Formatting**: Maintains document structure and formatting
- **Multi-language Support**: Currently supports Japanese, easily extensible to other languages
- **Translation History**: Keep track of your translations
- **Batch Processing**: Handle multiple papers efficiently

## 🛠️ Tech Stack

### Backend
- **Framework**: Python FastAPI
- **PDF Processing**: PyPDF2, pdfplumber
- **Translation API**: OpenAI GPT-4 / Anthropic Claude
- **Database**: SQLite (can be upgraded to PostgreSQL)

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: CSS3 with modern animations
- **HTTP Client**: Axios

### DevOps
- **Containerization**: Docker & Docker Compose
- **Local Development**: Hot-reload enabled for both services

## 📋 Prerequisites

- Docker & Docker Compose (for containerized setup)
- Or alternatively:
  - Python 3.11+
  - Node.js 18+
  - npm or yarn

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/Airu-8/chemistry-paper-translator.git
cd chemistry-paper-translator

# Create .env file from example
cp .env.example .env

# Edit .env and add your API keys
# TRANSLATION_API_KEY=your_key_here
# TRANSLATION_API_PROVIDER=openai  # or 'claude'

# Start the application
docker-compose up --build

# Application will be available at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example ../.env
# Edit .env with your configuration

# Run the server
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_BASE_URL=http://localhost:8000" > .env

# Start development server
npm start
```

## 📝 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Backend
FASTAPI_ENV=development
DATABASE_URL=sqlite:///./chemistry_translator.db

# Translation API (choose one)
TRANSLATION_API_PROVIDER=openai  # or 'claude'
TRANSLATION_API_KEY=your_api_key_here

# Frontend
REACT_APP_API_BASE_URL=http://localhost:8000

# File Upload
MAX_UPLOAD_SIZE_MB=50

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 🔌 API Endpoints

### Upload PDF
```
POST /api/upload
Content-Type: multipart/form-data

Request:
- file: PDF file

Response:
{
  "filename": "paper.pdf",
  "file_id": "uuid",
  "size": 1024000,
  "message": "File uploaded successfully"
}
```

### Translate Paper
```
POST /api/translate
Content-Type: application/json

Request:
{
  "filename": "paper.pdf",
  "target_language": "Japanese",
  "preserve_formatting": true
}

Response:
{
  "translation_id": "uuid",
  "filename": "paper.pdf",
  "status": "completed",
  "progress": 1.0,
  "translated_text": "...",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Get Translation History
```
GET /api/history

Response:
[
  {
    "translation_id": "uuid",
    "filename": "paper.pdf",
    "target_language": "Japanese",
    "status": "completed",
    "created_at": "2024-01-01T00:00:00",
    "file_size": 1024000,
    "page_count": 20
  }
]
```

### Get Specific Translation
```
GET /api/translation/{translation_id}

Response:
{
  "translation_id": "uuid",
  "filename": "paper.pdf",
  "status": "completed",
  "progress": 1.0,
  "translated_text": "...",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## 📚 API Documentation

Once the backend is running, visit:
```
http://localhost:8000/docs
```

This provides interactive API documentation via Swagger UI.

## 🔐 API Keys

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `.env`: `TRANSLATION_API_KEY=sk-...`
4. Set provider: `TRANSLATION_API_PROVIDER=openai`

### Anthropic Claude
1. Go to https://console.anthropic.com
2. Create a new API key
3. Add to `.env`: `TRANSLATION_API_KEY=sk-ant-...`
4. Set provider: `TRANSLATION_API_PROVIDER=claude`

## 📦 Project Structure

```
chemistry-paper-translator/
├── backend/                 # Python FastAPI application
│   ├── app/
│   │   ├── main.py         # FastAPI app initialization
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── models/         # Pydantic schemas
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
├── frontend/               # React TypeScript application
│   ├── src/
│   │   ├── pages/         # Page components
│   │   ├── styles/        # CSS files
│   │   └── App.tsx        # Main app component
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml     # Multi-container setup
├── .env.example           # Environment template
└── README.md
```

## 🧪 Testing

### Test Backend
```bash
cd backend
pip install pytest pytest-asyncio
pytest
```

### Test Frontend
```bash
cd frontend
npm test
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process using port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process using port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### API Connection Issues
- Ensure backend is running: `http://localhost:8000/health`
- Check CORS settings in `.env`
- Verify `REACT_APP_API_BASE_URL` in frontend `.env`

### Translation Errors
- Verify API key is valid and has sufficient credits
- Check API provider setting matches your key
- Review rate limits for your API plan

## 🗺️ Roadmap

- [ ] Batch processing for multiple files
- [ ] PDF generation for translated documents
- [ ] Database integration (PostgreSQL)
- [ ] User authentication and profiles
- [ ] Translation memory and terminology database
- [ ] Support for additional languages
- [ ] Chemical structure recognition and preservation
- [ ] Advanced formatting and layout preservation
- [ ] Mobile app
- [ ] CI/CD pipeline

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an GitHub issue.

## 🙏 Acknowledgments

- FastAPI framework
- React community
- PyPDF2 and pdfplumber libraries
- OpenAI and Anthropic APIs
