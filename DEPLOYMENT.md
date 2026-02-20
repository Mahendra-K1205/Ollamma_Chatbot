# 🚀 Production Deployment Guide

## Architecture Overview

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Vercel        │      │  Your Server     │      │   Ollama        │
│  (Frontend)     │─────▶│  (API Proxy)     │─────▶│   (LLM Models)  │
│   Next.js       │      │  Docker/VPS      │      │   GPU Server    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

**Important:** Ollama requires a persistent server with GPU/CPU. It CANNOT run on Vercel directly.

## Deployment Options

### Option 1: Vercel Frontend + Your Ollama Server (Recommended)

#### Step 1: Deploy Ollama Backend

**On your server (VPS/Cloud/Local):**

```bash
# Using Docker
docker-compose up -d

# Or manual installation
ollama serve
ollama pull llama3.2
```

**Make Ollama accessible:**
```bash
# Allow external connections
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
```

**Secure with reverse proxy (nginx):**
```nginx
server {
    listen 443 ssl;
    server_name ollama.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:11434;
        proxy_set_header Host $host;
    }
}
```

#### Step 2: Deploy Frontend to Vercel

```bash
cd web
npm install

# Deploy to Vercel
npx vercel --prod
```

**Set environment variable in Vercel:**
- Go to Vercel Dashboard → Settings → Environment Variables
- Add: `OLLAMA_API_URL` = `https://ollama.yourdomain.com`

### Option 2: Full Docker Deployment (VPS/Cloud)

```bash
# Clone repo
git clone <your-repo>
cd OLLAMA_CHATBOT

# Start everything
docker-compose up -d

# Pull model
docker exec ollama ollama pull llama3.2
```

Access at: `http://your-server-ip:8501`

### Option 3: Kubernetes Deployment

```bash
# Apply manifests
kubectl apply -f k8s/

# Expose service
kubectl port-forward svc/ollama-chatbot 8501:8501
```

## CI/CD Setup

### GitHub Actions

1. **Add secrets to GitHub:**
   - Go to Settings → Secrets → Actions
   - Add:
     - `DOCKER_USERNAME`
     - `DOCKER_PASSWORD`

2. **Push to trigger pipeline:**
```bash
git add .
git commit -m "Deploy"
git push origin main
```

Pipeline will:
- ✅ Run tests
- ✅ Lint code
- ✅ Build Docker image
- ✅ Push to Docker Hub

### Vercel Auto-Deploy

1. **Connect GitHub to Vercel:**
   - Go to vercel.com
   - Import your repository
   - Set root directory to `web/`
   - Add environment variable: `OLLAMA_API_URL`

2. **Auto-deploy on push:**
   - Every push to `main` triggers deployment
   - Preview deployments for PRs

## Environment Variables

### Backend (.env)
```bash
OLLAMA_API_URL=http://localhost:11434
```

### Frontend (Vercel)
```bash
OLLAMA_API_URL=https://your-ollama-server.com
```

## Testing

```bash
# Run unit tests
pytest tests/

# Test backend
python test_backend.py

# Test Docker build
docker build -t ollama-chatbot .
docker run -p 8501:8501 ollama-chatbot
```

## Monitoring

### Health Checks

```bash
# Ollama health
curl http://localhost:11434/api/tags

# App health
curl http://localhost:8501/_stcore/health
```

### Logs

```bash
# Docker logs
docker logs ollama-chatbot
docker logs ollama

# Vercel logs
vercel logs
```

## Scaling

### Horizontal Scaling
- Deploy multiple Ollama instances
- Use load balancer (nginx/HAProxy)
- Share models via NFS

### Vertical Scaling
- Use GPU instances (AWS p3, GCP A100)
- Increase RAM for larger models
- Use faster storage (NVMe SSD)

## Security

### API Security
```typescript
// Add API key authentication
export async function POST(request: Request) {
  const apiKey = request.headers.get('x-api-key');
  if (apiKey !== process.env.API_KEY) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }
  // ... rest of code
}
```

### Rate Limiting
```bash
# nginx rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
```

## Cost Optimization

### Cloud Providers
- **AWS EC2 g4dn.xlarge**: ~$0.50/hr (GPU)
- **GCP n1-standard-4**: ~$0.19/hr (CPU only)
- **DigitalOcean**: $48/month (8GB RAM)

### Model Selection
- **Small models** (phi, mistral): 2-4GB RAM
- **Medium models** (llama3.2): 4-8GB RAM
- **Large models** (llama3 70B): 40GB+ RAM

## Troubleshooting

### Vercel Deployment Issues
```bash
# Check build logs
vercel logs

# Test locally
npm run build
npm start
```

### Docker Issues
```bash
# Rebuild without cache
docker-compose build --no-cache

# Check container logs
docker logs -f ollama-chatbot
```

### Connection Issues
```bash
# Test Ollama connectivity
curl -X POST http://your-server:11434/api/chat \
  -d '{"model":"llama3.2","messages":[{"role":"user","content":"hi"}]}'
```

## Quick Start Commands

```bash
# Local development
docker-compose up -d
python app_tkinter.py

# Production deployment
git push origin main  # Triggers CI/CD
vercel --prod         # Deploy frontend

# Test everything
pytest tests/
python test_backend.py
```

## Support

- **GitHub Issues**: Report bugs
- **Discussions**: Ask questions
- **Wiki**: Detailed guides

---

**Ready for production! 🎉**
