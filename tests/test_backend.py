import pytest
from unittest.mock import Mock, patch
from ollama_backend import OllamaBackend


class TestOllamaBackend:
    
    def test_init(self):
        backend = OllamaBackend()
        assert backend.base_url == "http://localhost:11434"
        assert backend.chat_history == []
    
    def test_set_model(self):
        backend = OllamaBackend()
        backend.chat_history = [{"role": "user", "content": "test"}]
        backend.set_model("llama3.2")
        assert backend.model == "llama3.2"
        assert backend.chat_history == []
    
    def test_clear_history(self):
        backend = OllamaBackend()
        backend.chat_history = [{"role": "user", "content": "test"}]
        backend.clear_history()
        assert backend.chat_history == []
    
    @patch('ollama_backend.requests.get')
    def test_get_available_models(self, mock_get):
        mock_get.return_value.json.return_value = {
            "models": [{"name": "llama3.2:latest"}]
        }
        backend = OllamaBackend()
        models = backend.get_available_models()
        assert models == ["llama3.2:latest"]
    
    @patch('ollama_backend.requests.post')
    def test_send_message_success(self, mock_post):
        mock_post.return_value.json.return_value = {
            "message": {"content": "Hello!"}
        }
        backend = OllamaBackend(model="llama3.2")
        response = backend.send_message("Hi")
        assert response == "Hello!"
        assert len(backend.chat_history) == 2
    
    def test_send_message_empty(self):
        backend = OllamaBackend(model="llama3.2")
        response = backend.send_message("")
        assert response == "Please enter a message."
