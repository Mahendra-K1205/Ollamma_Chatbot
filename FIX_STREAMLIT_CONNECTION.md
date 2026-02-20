# Fix "Cannot connect to Ollama" on Streamlit Cloud

## Problem
Streamlit Cloud can't access `http://localhost:11434` because Ollama is on your local machine.

## Solutions

### Option 1: Use ngrok (Quick Test)

```bash
# On your local machine where Ollama is running
ollama serve

# In another terminal
ngrok http 11434
```

Copy the ngrok URL (e.g., `https://abc123.ngrok-free.app`)

**In Streamlit Cloud:**
1. Go to your app settings
2. Click "Secrets"
3. Add:
```
OLLAMA_API_URL = "https://abc123.ngrok-free.app"
```
4. Save and reboot app

⚠️ **Note:** ngrok free URLs expire after 2 hours

### Option 2: Deploy Ollama on VPS (Production)

**1. Get a VPS (DigitalOcean, AWS, etc.)**

**2. Install Ollama:**
```bash
ssh user@your-server-ip

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Allow external connections
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &

# Pull model
ollama pull llama3.2
```

**3. Configure Streamlit Cloud:**
- Secrets: `OLLAMA_API_URL = "http://your-server-ip:11434"`

### Option 3: Run Streamlit Locally (Easiest)

```bash
# Just run locally instead
streamlit run app_streamlit.py
```

This works with your local Ollama without any configuration.

## Recommended Approach

**For testing:** Use Option 3 (run locally)
**For production:** Use Option 2 (VPS with Ollama)

---

**Bottom line:** Streamlit Cloud needs a public URL to reach Ollama. You can't use localhost.
