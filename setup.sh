#!/bin/bash

echo "🚀 Ollama Chatbot - Production Setup"
echo "===================================="

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install Python 3.8+"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker not found. Install for containerized deployment."
fi

echo "✅ Prerequisites OK"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run tests
echo ""
echo "Running tests..."
pytest tests/ -v

# Check Ollama
echo ""
echo "Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
    MODELS=$(curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
    echo "Available models: $MODELS"
else
    echo "⚠️  Ollama not running. Start with: ollama serve"
fi

# Setup web
echo ""
echo "Setting up Next.js frontend..."
cd web
if command -v npm &> /dev/null; then
    npm install
    echo "✅ Web dependencies installed"
else
    echo "⚠️  npm not found. Install Node.js for web deployment."
fi
cd ..

# Create .env
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env created. Update with your settings."
fi

echo ""
echo "===================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start Ollama: ollama serve"
echo "2. Pull model: ollama pull llama3.2"
echo "3. Run app: python app_tkinter.py"
echo "4. Or Docker: docker-compose up -d"
echo "5. Or Web: cd web && npm run dev"
echo ""
echo "For production deployment, see DEPLOYMENT.md"
