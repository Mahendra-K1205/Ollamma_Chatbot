# Next.js Frontend for Ollama Chatbot

## Local Development

```bash
npm install
npm run dev
```

Open http://localhost:3000

## Environment Variables

Create `.env.local`:

```bash
OLLAMA_API_URL=http://localhost:11434
```

## Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

Or connect GitHub repo to Vercel for auto-deployment.

## Configuration

Set environment variable in Vercel:
- `OLLAMA_API_URL` = Your Ollama server URL

## Build

```bash
npm run build
npm start
```
