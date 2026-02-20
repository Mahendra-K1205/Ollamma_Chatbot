"""
Ollama Chatbot - Tkinter Desktop GUI
Clean, modern desktop interface for local LLM chat.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from ollama_backend import OllamaBackend


class ChatbotGUI:
    """Tkinter GUI for Ollama chatbot."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama Chatbot")
        self.root.geometry("800x700")
        self.root.configure(bg="#1e1e1e")
        
        # Initialize backend
        self.backend = OllamaBackend()
        self.is_loading = False
        
        # Setup UI
        self._setup_ui()
        self._load_models()
    
    def _setup_ui(self):
        """Create UI components."""
        
        # Top bar - Model selection
        top_frame = tk.Frame(self.root, bg="#2d2d2d", height=60)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        top_frame.pack_propagate(False)
        
        tk.Label(top_frame, text="Model:", bg="#2d2d2d", fg="white", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(top_frame, textvariable=self.model_var, state="readonly", width=25)
        self.model_dropdown.pack(side=tk.LEFT, padx=5)
        self.model_dropdown.bind("<<ComboboxSelected>>", self._on_model_change)
        
        clear_btn = tk.Button(top_frame, text="Clear Chat", command=self._clear_chat, 
                             bg="#d9534f", fg="white", font=("Arial", 10, "bold"), 
                             relief=tk.FLAT, cursor="hand2", padx=15)
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # Chat display area
        chat_frame = tk.Frame(self.root, bg="#1e1e1e")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, state=tk.DISABLED,
            bg="#2b2b2b", fg="#e0e0e0", font=("Consolas", 10),
            relief=tk.FLAT, padx=10, pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground="#4fc3f7", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("bot", foreground="#81c784", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("error", foreground="#e57373", font=("Arial", 10, "italic"))
        self.chat_display.tag_config("loading", foreground="#ffd54f", font=("Arial", 10, "italic"))
        
        # Input area
        input_frame = tk.Frame(self.root, bg="#2d2d2d")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_box = tk.Text(input_frame, height=3, wrap=tk.WORD, 
                                bg="#3c3c3c", fg="white", font=("Arial", 11),
                                relief=tk.FLAT, padx=10, pady=10)
        self.input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.input_box.bind("<Return>", self._on_enter_key)
        
        self.send_btn = tk.Button(input_frame, text="Send", command=self._send_message,
                                 bg="#5cb85c", fg="white", font=("Arial", 12, "bold"),
                                 relief=tk.FLAT, cursor="hand2", width=10, height=2)
        self.send_btn.pack(side=tk.RIGHT)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", bg="#2d2d2d", fg="#aaa", 
                                     font=("Arial", 9), anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=10, pady=(0, 5))
    
    def _load_models(self):
        """Load available models from Ollama."""
        try:
            models = self.backend.get_available_models()
            if models:
                self.model_dropdown["values"] = models
                self.model_dropdown.current(0)
                self.backend.set_model(models[0])
                self._update_status(f"Loaded {len(models)} models")
            else:
                self._update_status("No models found", error=True)
                messagebox.showwarning("No Models", "No Ollama models found. Please pull a model first.")
        except ConnectionError as e:
            self._update_status("Ollama not running", error=True)
            messagebox.showerror("Connection Error", str(e))
    
    def _on_model_change(self, event):
        """Handle model selection change."""
        model = self.model_var.get()
        self.backend.set_model(model)
        self._update_status(f"Switched to {model} (history cleared)")
        # Clear display
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _on_enter_key(self, event):
        """Handle Enter key press (Shift+Enter for newline)."""
        if not event.state & 0x1:  # No Shift key
            self._send_message()
            return "break"
    
    def _send_message(self):
        """Send user message to backend."""
        if self.is_loading:
            return
        
        message = self.input_box.get("1.0", tk.END).strip()
        if not message:
            return
        
        # Display user message
        self._display_message("You", message, "user")
        self.input_box.delete("1.0", tk.END)
        
        # Show loading indicator
        self.is_loading = True
        self._display_message("Bot", "Thinking... (First request may take 1-2 minutes to load model)", "loading")
        self._update_status("Generating response... Please wait...")
        self.send_btn.config(state=tk.DISABLED, text="Wait...")
        
        # Send request in background thread
        threading.Thread(target=self._get_response, args=(message,), daemon=True).start()
    
    def _get_response(self, message: str):
        """Get response from backend (runs in thread)."""
        try:
            response = self.backend.send_message(message)
            self.root.after(0, self._handle_response, response)
        except Exception as e:
            self.root.after(0, self._handle_error, str(e))
    
    def _handle_response(self, response: str):
        """Handle successful response."""
        # Remove loading message
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("end-2l", "end-1l")
        self.chat_display.config(state=tk.DISABLED)
        
        # Display bot response
        self._display_message("Bot", response, "bot")
        self._update_status("Ready")
        self.is_loading = False
        self.send_btn.config(state=tk.NORMAL, text="Send")
        self.input_box.focus()
    
    def _handle_error(self, error: str):
        """Handle error response."""
        # Remove loading message
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("end-2l", "end-1l")
        self.chat_display.config(state=tk.DISABLED)
        
        # Display error
        self._display_message("Error", error, "error")
        self._update_status("Error occurred", error=True)
        self.is_loading = False
        self.send_btn.config(state=tk.NORMAL, text="Send")
    
    def _display_message(self, sender: str, message: str, tag: str):
        """Display message in chat area."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _clear_chat(self):
        """Clear chat history and display."""
        if messagebox.askyesno("Clear Chat", "Clear all chat history?"):
            self.backend.clear_history()
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self._update_status("Chat cleared")
    
    def _update_status(self, message: str, error: bool = False):
        """Update status bar."""
        color = "#e57373" if error else "#81c784"
        self.status_label.config(text=message, fg=color)


def main():
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
