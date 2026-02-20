"""Quick test script to verify Ollama backend works"""

from ollama_backend import OllamaBackend
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

print("Testing Ollama Backend...")
print("-" * 50)

try:
    # Initialize backend
    backend = OllamaBackend()
    print("[OK] Backend initialized")
    
    # Get models
    models = backend.get_available_models()
    print(f"[OK] Found {len(models)} models: {models}")
    
    if models:
        backend.set_model(models[0])
        print(f"[OK] Using model: {models[0]}")
        
        # Send test message
        print("\nSending test message...")
        print("(This may take 1-2 minutes on first run)")
        response = backend.send_message("Say 'Hello' in one word")
        print(f"[OK] Got response: {response}")
        print("\n[SUCCESS] All tests passed!")
    else:
        print("[ERROR] No models found. Run: ollama pull llama3.2")
        
except Exception as e:
    print(f"[ERROR] {e}")
