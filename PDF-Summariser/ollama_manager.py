import os
import subprocess
import time
from tkinter import messagebox 

# https://www.quora.com/How-do-you-run-an-exe-from-a-Python-file-Python-exe-development

class OllamaManager:
    def __init__(self, base_path=None):
        """Initializes OllamaManager with the correct path to Ollama.exe."""
        local_appdata = os.getenv("LOCALAPPDATA")  # Get LocalAppData path dynamically
        default_path = os.path.join(local_appdata, "PDF-Summariser", "Ollama", "ollama.exe")
        
        self.base_path = default_path  # Correct path
        
        print(f"Base path to Ollama: {self.base_path}")  # Debugging line to check the path

    def is_running(self):
        """Checks if Ollama is already running on port 11434."""
        try:
            result = subprocess.run(
                ["powershell", "-Command", "netstat -ano | findstr :11434"],
                capture_output=True, text=True
            )
            return "LISTENING" in result.stdout
        except Exception as e:
            messagebox.showerror("Error", f"🚨 Error checking if Ollama is running: {e}")
            print(f"🚨 Error checking if Ollama is running: {e}")
            return False

    def stop(self):
        """Stops Ollama if it is running."""
        try:
            result = subprocess.run(
                ["powershell", "-Command", "netstat -ano | findstr :11434"],
                capture_output=True, text=True
            )
            if result.stdout:
                for line in result.stdout.strip().split("\n"):
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]  # Get the process ID (PID)
                        subprocess.run(["taskkill", "/PID", pid, "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        print(f"🛑 Stopped Ollama process with PID: {pid}")
        except Exception as e:
            print(f"🚨 Error stopping Ollama: {e}")
            messagebox.showerror("Error", f"🚨 Error stopping Ollama: {e}")

    def start(self):
        """Stops any existing Ollama process and starts a new one."""
        self.stop()  # Stop any existing instance first

        if self.is_running():
            print("✅ Ollama is already running. No need to start it again.")
            messagebox.showinfo("Info Ollama", "✅ Ollama is already running. No need to start it again.")
            return
        
        if not os.path.isfile(self.base_path):
            print(f"❌ Ollama executable not found at: {self.base_path}")
            messagebox.showerror("Error", f"❌ Ollama executable not found at: {self.base_path}")
            return
        
        ollama_dir = os.path.dirname(self.base_path)

        print("🚀 Starting Ollama...")
        messagebox.showinfo("Ollama running", "🚀 Starting Ollama...")

        try:
            subprocess.Popen([self.base_path, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=ollama_dir, shell=False)

            # Wait for Ollama to start (this might need a bit of adjustment)
            time.sleep(5)

            if self.is_running():
                print("✅ Ollama started successfully.")
                messagebox.showinfo("Ollama running", "✅ Ollama started successfully.")
            else:
                print("⚠️ Error: Ollama failed to start.")

        except Exception as e:
            print(f"🚨 Error while starting Ollama: {e}")
            messagebox.showerror("Error", f"🚨 Error while starting Ollama: {e}")
    
    def pull_model(self, model_name):
        """Télécharge un modèle Ollama via 'ollama pull <model>'."""
        if not os.path.isfile(self.base_path):
            print(f"❌ Ollama executable not found at: {self.base_path}")
            messagebox.showerror("Error", f"❌ Ollama executable not found at: {self.base_path}")
            return

        print(f"⬇️ Pulling model: {model_name}...")
        messagebox.showinfo("Ollama", f"⬇️ Pulling model: {model_name}...")

        try:
            result = subprocess.run(
                [self.base_path, "pull", model_name],
                capture_output=True,
                text=True,
                shell=False
            )

            if result.returncode == 0:
                print(f"✅ Model '{model_name}' pulled successfully.")
                messagebox.showinfo("Ollama", f"✅ Model '{model_name}' pulled successfully.")
            else:
                print(f"⚠️ Error pulling model '{model_name}':\n{result.stderr}")
                messagebox.showerror("Ollama", f"⚠️ Error pulling model '{model_name}':\n{result.stderr}")

        except Exception as e:
            print(f"🚨 Error while pulling model: {e}")
            messagebox.showerror("Error", f"🚨 Error while pulling model: {e}")

