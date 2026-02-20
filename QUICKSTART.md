# \ud83d\ude80 Quick Start - Production Deployment

## 1. Local Development

```bash
# Clone and setup
git clone <your-repo>
cd OLLAMA_CHATBOT
pip install -r requirements.txt

# Start Ollama
ollama serve
ollama pull llama3.2

# Run app
python app_tkinter.py
```

## 2. Docker Deployment

```bash
# Start everything
docker-compose up -d

# Pull model
docker exec ollama ollama pull llama3.2

# Access at http://localhost:8501
```

## 3. Vercel Deployment (Frontend Only)

```bash
# Setup Ollama on your server first
# Then deploy frontend:

cd web
npm install
npx vercel --prod

# Add environment variable in Vercel:
# OLLAMA_API_URL = https://your-ollama-server.com
```

## 4. Full Production Stack

### Backend Server (Your VPS/Cloud)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &

# Pull models
ollama pull llama3.2

# Run API server
python api_server.py
```

### Frontend (Vercel)

```bash
cd web
vercel --prod
```

Set environment variable:
- `OLLAMA_API_URL` = `http://your-server-ip:8000`

## 5. GitHub CI/CD Setup

```bash
# Add secrets to GitHub repo:
# Settings > Secrets > Actions

DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_token

# Push to trigger pipeline
git push origin main
```

## Architecture

```
User Browser
    \u2193
Vercel (Next.js Frontend)
    \u2193
Your Server (FastAPI/Ollama)
    \u2193
Ollama LLM Models
```

## Quick Commands

```bash
# Test
make test

# Lint
make lint

# Build Docker
make docker-build

# Deploy
make deploy-vercel
```

## Important Notes

\u26a0\ufe0f **Ollama CANNOT run on Vercel** - it needs a persistent server with GPU/CPU

\u2705 **Solution**: Deploy frontend to Vercel, backend to your own server

\ud83d\udcb0 **Cost**: Frontend free on Vercel, backend ~$5-50/month depending on server
