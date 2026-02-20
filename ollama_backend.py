"""
Ollama Backend Module
Handles communication with Ollama API and manages chat history.
"""

import requests
from typing import List, Dict, Optional


class OllamaBackend:
    """Backend handler for Ollama LLM interactions."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = None):
        """
        Initialize Ollama backend.
        
        Args:
            base_url: Ollama API base URL
            model: Model name to use (auto-detected if None)
        """
        self.base_url = base_url
        self.model = model
        self.chat_history: List[Dict[str, str]] = []
        
        # Auto-detect model if not specified
        if self.model is None:
            try:
                models = self.get_available_models()
                if models:
                    self.model = models[0]
            except:
                pass
    
    def set_model(self, model: str):
        """Change the active model and clear history."""
        self.model = model
        self.clear_history()  # Clear history when switching models
    
    def get_available_models(self) -> List[str]:
        """
        Fetch available models from Ollama.
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Cannot connect to Ollama. Ensure it's running: ollama serve")
    
    def send_message(self, prompt: str) -> str:
        """
        Send a message to Ollama and get response.
        
        Args:
            prompt: User input text
            
        Returns:
            Model's response text
        """
        if not prompt.strip():
            return "Please enter a message."
        
        if not self.model:
            raise Exception("No model selected. Please select a model first.")
        
        # Add user message to history
        self.chat_history.append({"role": "user", "content": prompt})
        
        try:
            # Send request to Ollama
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": self.chat_history,
                    "stream": False
                },
                timeout=300  # 5 minutes for first load
            )
            response.raise_for_status()
            
            # Extract assistant response
            result = response.json()
            assistant_message = result.get("message", {}).get("content", "")
            
            if not assistant_message:
                raise Exception("Empty response from model")
            
            # Add to history
            self.chat_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except requests.exceptions.Timeout:
            self.chat_history.pop()  # Remove user message on error
            raise TimeoutError("Request timed out. Model may be loading (first request can take 1-2 minutes).")
        except requests.exceptions.ConnectionError:
            self.chat_history.pop()
            raise ConnectionError("Cannot connect to Ollama. Ensure it's running: ollama serve")
        except requests.exceptions.RequestException as e:
            self.chat_history.pop()
            error_msg = str(e)
            if "404" in error_msg:
                raise Exception(f"Model '{self.model}' not found. Pull it with: ollama pull {self.model}")
            raise Exception(f"Error: {error_msg}")
    
    def clear_history(self):
        """Clear chat history."""
        self.chat_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get current chat history."""
        return self.chat_history
