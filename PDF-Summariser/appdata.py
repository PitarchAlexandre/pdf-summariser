import os
import subprocess
import time
from tkinter import messagebox

# https://www.geeksforgeeks.org/run-one-python-script-from-another-in-python/

class OllamaManager:
    def __init__(self, base_path=None):
        """Initializes the Ollama manager with a specific path if provided."""
        
        # Get the LocalAppData path dynamically (C:\Users\<Utilisateur>\AppData\Local)
        local_appdata = os.getenv("LOCALAPPDATA")

        # Construct the full path to Ollama.exe
        appdata_path = os.path.join(local_appdata, "PDF-Summariser", "Ollama", "ollama.exe")

        # Use the provided path or default to the AppData path
        self.base_path = base_path or appdata_path

    def is_running(self):
        """Checks if Ollama is already running."""
        print(self.base_path)
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            return result.returncode == 0  # If return code is 0, Ollama is running
        except FileNotFoundError:
            return False

    def start(self):
        """Starts Ollama if it is not already running."""
        if self.is_running():
            print("Ollama is already running.")
            return

        messagebox.showinfo("Ollama", "The application is starting Ollama.")

        if not os.path.exists(self.base_path):
            print(f"Ollama not found at: {self.base_path}")
            return

        print("Starting Ollama...")
        subprocess.Popen([self.base_path, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait a few seconds to ensure it starts properly
        time.sleep(3)

        if self.is_running():
            print("Ollama started successfully.")
        else:
            print("Error: Ollama failed to start.")
            messagebox.showwarning("Ollama", "Failed to start Ollama.")