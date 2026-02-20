@echo off
echo ========================================
echo Ollama Chatbot - Production Setup
echo ========================================

echo Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.8+
    exit /b 1
)
echo [OK] Python found

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Running tests...
pytest tests/ -v

echo.
echo Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama not running. Start with: ollama serve
) else (
    echo [OK] Ollama is running
)

echo.
echo Setting up Next.js frontend...
cd web
npm --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] npm not found. Install Node.js for web deployment.
) else (
    npm install
    echo [OK] Web dependencies installed
)
cd ..

if not exist .env (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo [OK] .env created. Update with your settings.
)

echo.
echo ========================================
echo Setup complete!
echo.
echo Next steps:
echo 1. Start Ollama: ollama serve
echo 2. Pull model: ollama pull llama3.2
echo 3. Run app: python app_tkinter.py
echo 4. Or Docker: docker-compose up -d
echo 5. Or Web: cd web ^&^& npm run dev
echo.
echo For production deployment, see DEPLOYMENT.md
pause
