# 🚀 Deploy to Streamlit Cloud

## Prerequisites

⚠️ **Important:** Streamlit Cloud cannot run Ollama directly. You need:
1. **Ollama server** running on your own machine/VPS
2. **Publicly accessible URL** for your Ollama server

## Setup Ollama Server

### Option 1: Local Machine (for testing)

```bash
# Start Ollama
ollama serve

# Use ngrok to expose it
ngrok http 11434
# Copy the https URL (e.g., https://abc123.ngrok.io)
```

### Option 2: VPS/Cloud Server (recommended)

```bash
# SSH to your server
ssh user@your-server

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Allow external connections
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &

# Pull model
ollama pull llama3.2

# Your Ollama URL: http://your-server-ip:11434
```

## Deploy to Streamlit Cloud

### 1. Push to GitHub

```bash
git add .
git commit -m "Ready for Streamlit Cloud"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select your repository: `Mahendra-K1205/Ollamma_Chatbot`
4. Main file path: `app_streamlit.py`
5. Click "Advanced settings"
6. Add secret:
   ```
   OLLAMA_API_URL = "http://your-server-ip:11434"
   ```
7. Click "Deploy"

### 3. Access Your App

Your app will be live at: `https://your-app.streamlit.app`

## Alternative: Run Locally

```bash
streamlit run app_streamlit.py
```

## Troubleshooting

### Connection Error

- Ensure Ollama server is running
- Check firewall allows port 11434
- Verify OLLAMA_API_URL is correct

### No Models Found

```bash
# On your Ollama server
ollama pull llama3.2
```

## Architecture

```
Streamlit Cloud (Frontend)
    ↓
Your Server (Ollama)
    ↓
LLM Models
```

---

**Cost:** Streamlit Cloud is FREE, but you need a server for Ollama (~$5-50/month)
