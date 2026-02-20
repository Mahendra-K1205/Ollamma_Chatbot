# 🚀 Getting Started - Production Deployment

## Overview

Your Ollama Chatbot is now **production-ready** with:
- ✅ CI/CD pipelines (GitHub Actions)
- ✅ Docker & Kubernetes support
- ✅ Vercel deployment ready
- ✅ Multiple deployment options
- ✅ Comprehensive testing
- ✅ Full documentation

## Important: Ollama Deployment Limitation

⚠️ **Ollama CANNOT run on Vercel** because:
- Vercel is serverless (no persistent processes)
- Ollama needs GPU/CPU and stays loaded in memory
- Models are 2GB+ in size

✅ **Solution:**
- Deploy **frontend** to Vercel (FREE)
- Deploy **backend** to your own server (VPS/Cloud)

## Quick Start (3 Options)

### Option 1: Local Development (Fastest)

```bash
# 1. Setup
setup.bat  # Windows
# or
./setup.sh  # Linux/Mac

# 2. Start Ollama
ollama serve
ollama pull llama3.2

# 3. Run app
python app_tkinter.py
```

### Option 2: Docker (Recommended)

```bash
# Start everything
docker-compose up -d

# Pull model
docker exec ollama ollama pull llama3.2

# Access at http://localhost:8501
```

### Option 3: Production (Vercel + Your Server)

**Step 1: Deploy Backend (Your Server)**
```bash
# SSH to your VPS
ssh user@your-server

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &

# Pull model
ollama pull llama3.2

# Optional: Run FastAPI proxy
git clone <your-repo>
cd OLLAMA_CHATBOT
pip install -r requirements.txt
python api_server.py
```

**Step 2: Deploy Frontend (Vercel)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd web
vercel --prod
```

**Step 3: Configure**
- In Vercel Dashboard → Settings → Environment Variables
- Add: `OLLAMA_API_URL` = `http://your-server-ip:11434`

## GitHub CI/CD Setup

### 1. Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/ollama-chatbot.git
git push -u origin main
```

### 2. Add GitHub Secrets

Go to: **Settings → Secrets and variables → Actions**

Add these secrets:
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub token
- `VERCEL_TOKEN` - Get from vercel.com/account/tokens
- `VERCEL_ORG_ID` - Run `vercel` in web/ folder to get
- `VERCEL_PROJECT_ID` - Run `vercel` in web/ folder to get

### 3. Push to Trigger Pipeline

```bash
git push origin main
```

Pipeline will automatically:
- ✅ Run tests
- ✅ Lint code
- ✅ Build Docker image
- ✅ Push to Docker Hub
- ✅ Deploy to Vercel

## Vercel Auto-Deploy Setup

### Method 1: Vercel CLI

```bash
cd web
npm install
vercel
```

Follow prompts to link GitHub repo.

### Method 2: Vercel Dashboard

1. Go to vercel.com
2. Click "Add New Project"
3. Import your GitHub repository
4. Set **Root Directory** to `web/`
5. Add environment variable: `OLLAMA_API_URL`
6. Deploy!

Every push to `main` will auto-deploy.

## Architecture

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       ↓
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Vercel     │────→│ Your Server  │────→│   Ollama     │
│  (Frontend)  │     │  (Optional   │     │   (LLM)      │
│   Next.js    │     │   FastAPI)   │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
    FREE                $5-50/month          Included
```

## Testing

```bash
# Backend test
python test_backend.py

# Unit tests
pytest tests/ -v

# Lint
flake8 .

# All tests
make test
```

## Deployment Checklist

- [ ] Tests passing locally
- [ ] Ollama running and accessible
- [ ] GitHub repo created
- [ ] CI/CD secrets added
- [ ] Backend deployed (if using separate server)
- [ ] Frontend deployed to Vercel
- [ ] Environment variables configured
- [ ] Domain configured (optional)
- [ ] SSL enabled (automatic on Vercel)
- [ ] Monitoring setup (optional)

## Common Commands

```bash
# Development
python app_tkinter.py              # Desktop app
streamlit run app_streamlit.py     # Web app
cd web && npm run dev              # Next.js dev

# Docker
docker-compose up -d               # Start all
docker-compose logs -f             # View logs
docker-compose down                # Stop all

# Testing
pytest tests/                      # Run tests
make test                          # Run all tests
make lint                          # Lint code

# Deployment
vercel --prod                      # Deploy to Vercel
make deploy-vercel                 # Deploy via Makefile
```

## Monitoring

### Health Checks

```bash
# Ollama
curl http://your-server:11434/api/tags

# FastAPI
curl http://your-server:8000/health

# Vercel
curl https://your-app.vercel.app
```

### Logs

```bash
# Docker
docker logs ollama-chatbot
docker logs ollama

# Vercel
vercel logs
```

## Troubleshooting

### CI/CD Pipeline Failing

1. Check GitHub Actions logs
2. Verify secrets are set correctly
3. Ensure tests pass locally first

### Vercel Deployment Issues

1. Check build logs in Vercel dashboard
2. Verify `OLLAMA_API_URL` is set
3. Test API endpoint manually

### Connection Issues

1. Ensure Ollama is accessible externally
2. Check firewall rules
3. Verify CORS settings in API

## Cost Breakdown

| Component | Service | Cost |
|-----------|---------|------|
| Frontend | Vercel | FREE |
| Backend | DigitalOcean Droplet | $6/month |
| Backend | AWS EC2 t3.medium | ~$30/month |
| Backend | GCP e2-medium | ~$25/month |
| Domain | Namecheap | ~$10/year |
| SSL | Let's Encrypt | FREE |

**Total:** $6-30/month

## Scaling

### Horizontal Scaling
- Multiple Ollama instances
- Load balancer (nginx)
- Kubernetes deployment

### Vertical Scaling
- Larger server (more RAM/CPU)
- GPU instance for faster inference
- SSD storage for models

## Security

- ✅ HTTPS enabled (Vercel automatic)
- ✅ Environment variables for secrets
- ✅ CORS configured
- ✅ Rate limiting (optional)
- ✅ API authentication (optional)

## Next Steps

1. **Test locally** - Ensure everything works
2. **Push to GitHub** - Enable CI/CD
3. **Deploy backend** - Setup Ollama server
4. **Deploy frontend** - Push to Vercel
5. **Configure domain** - Point to Vercel (optional)
6. **Monitor** - Setup alerts (optional)
7. **Scale** - Add resources as needed

## Support & Resources

- **Documentation:** README.md, DEPLOYMENT.md
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Ollama Docs:** https://ollama.ai/docs

---

**🎉 You're ready for production!**

Start with local development, then scale to production when ready.
