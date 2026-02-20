# 🤖 Ollama Local Chatbot

A production-ready local chatbot application using Ollama LLMs with both desktop (Tkinter) and web (Streamlit/Next.js) interfaces.

[![CI/CD](https://github.com/yourusername/ollama-chatbot/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/yourusername/ollama-chatbot/actions)
[![Docker](https://img.shields.io/docker/v/yourusername/ollama-chatbot)](https://hub.docker.com/r/yourusername/ollama-chatbot)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ Features

- 💬 Interactive chat with local LLM models
- 🔄 Conversation context maintained throughout session
- 🎨 Modern, clean UI with dark theme
- 📦 Model selection dropdown
- 🗑️ Clear chat functionality
- ⚡ Loading indicators
- 🛡️ Comprehensive error handling
- 🏗️ Modular, production-ready code structure
- 🚀 CI/CD pipeline with GitHub Actions
- 🐳 Docker & Kubernetes support
- ☁️ Vercel deployment ready
- 🧪 Unit tests & code coverage

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running

## 🚀 Installation

### Step 1: Install Ollama

**Windows:**
```bash
# Download and install from: https://ollama.ai/download
# Or use winget:
winget install Ollama.Ollama
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Pull an Ollama Model

```bash
# Start Ollama service (if not auto-started)
ollama serve

# In a new terminal, pull a model (choose one or more):
ollama pull llama3.2
ollama pull mistral
ollama pull codellama
ollama pull phi
```

### Step 3: Install Python Dependencies

```bash
# Navigate to project directory
cd "d:\Mahendra K\OLLAMA_CHATBOT"

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Test Backend (Optional)

```bash
# Verify everything works
python test_backend.py
```

## 🎮 Running the Application

### Option A: Tkinter Desktop App

```bash
python app_tkinter.py
```

### Option B: Streamlit Web App

```bash
streamlit run app_streamlit.py
```

### Option C: Next.js Web App (Production)

```bash
cd web
npm install
npm run dev
```

### Option D: Docker (All-in-One)

```bash
docker-compose up -d
```

### Option E: FastAPI Backend

```bash
python api_server.py
```

## 🚀 Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete production deployment guide including:
- Vercel deployment
- Docker deployment
- Kubernetes deployment
- CI/CD setup
- Monitoring & scaling

## 📖 Usage Guide

### Tkinter App

1. **Launch** the application
2. **Select Model** from dropdown (top bar)
3. **Type Message** in the input box at bottom
4. **Send** by clicking "Send" button or pressing Enter
5. **Clear Chat** using the "Clear Chat" button
6. **View History** in the scrollable chat area

### Streamlit App

1. **Launch** the application (opens in browser)
2. **Select Model** from sidebar
3. **Type Message** in the input field
4. **Send** by clicking "Send" or pressing Enter
5. **Clear Chat** using sidebar button
6. **Refresh Models** if you pull new models

## 🏗️ Project Structure

```
OLLAMA_CHATBOT/
├── .github/workflows/     # CI/CD pipelines
├── web/                   # Next.js frontend (Vercel)
├── tests/                 # Unit tests
├── ollama_backend.py      # Backend logic
├── app_tkinter.py         # Desktop GUI
├── app_streamlit.py       # Streamlit web GUI
├── api_server.py          # FastAPI server
├── Dockerfile             # Container image
├── docker-compose.yml     # Multi-container setup
├── k8s-deployment.yaml    # Kubernetes manifests
├── requirements.txt       # Python dependencies
├── DEPLOYMENT.md          # Production deployment guide
└── README.md              # This file
```

## 🔧 Configuration

### Change Ollama URL

If Ollama is running on a different host/port, modify in the app files:

```python
# In app_tkinter.py or app_streamlit.py
self.backend = OllamaBackend(base_url="http://your-host:port")
```

### Default Model

Change default model in `ollama_backend.py`:

```python
def __init__(self, base_url: str = "http://localhost:11434", model: str = "your-model"):
```

## 🐛 Troubleshooting

### "Cannot connect to Ollama"

**Solution:**
```bash
# Start Ollama service
ollama serve
```

### "No models found"

**Solution:**
```bash
# Pull at least one model
ollama pull llama3.2
```

### Chatbot not responding / Stuck on "Thinking..."

**Cause:** First request loads the model into memory (takes 1-2 minutes)

**Solution:**
- Wait patiently for first response (can take 1-2 minutes)
- Subsequent responses will be much faster
- Check Ollama is running: `ollama serve`
- Test backend: `python test_backend.py`

### Model name mismatch

**Solution:**
- Check installed models: `ollama list`
- Use exact model name from the list (e.g., `llama3.2:latest` not `llama3`)
- App auto-detects available models

### Port Already in Use (Streamlit)

**Solution:**
```bash
# Use different port
streamlit run app_streamlit.py --server.port 8502
```

### Slow Response Times

**Causes:**
- Large model size
- Limited CPU/RAM
- First request (model loading)

**Solutions:**
- Use smaller models (phi, mistral)
- Increase timeout in `ollama_backend.py`
- Wait for first request to complete

## 🎨 Customization

### Change UI Colors (Tkinter)

Edit color codes in `app_tkinter.py`:
```python
bg="#1e1e1e"  # Background
fg="#e0e0e0"  # Foreground text
```

### Change UI Theme (Streamlit)

Modify CSS in `app_streamlit.py` under `st.markdown()` section.

## 📦 Dependencies

- **requests**: HTTP client for Ollama API
- **streamlit**: Web UI framework (optional)
- **tkinter**: Desktop UI (included with Python)

## 🔒 Security Notes

- Application runs locally only
- No data sent to external servers
- All processing happens on your machine
- Chat history stored in memory only (cleared on exit)

## 📝 License

This project is open-source and available for personal and commercial use.

## 🤝 Contributing

Feel free to fork, modify, and improve this application!

## 📧 Support

For issues:
1. Check Ollama is running: `ollama serve`
2. Verify models installed: `ollama list`
3. Check Python version: `python --version` (3.8+ required)

---

**Enjoy chatting with your local AI! 🚀**
