import json
import requests

class OcrConfig():
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_file = self.parse_config(config_path)

    # Search the config file and 
    def parse_config(self, config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Le fichier de configuration {config_path} est introuvable.")
        except json.JSONDecodeError:
            raise ValueError("Erreur lors du décodage du fichier JSON.")
    
       # To have the first config(Ollama, Llama3.2)
    def get_default_key(self):
        try:
            return self.config_file["api_keys_ocr"][0]
        except (KeyError, IndexError):
            raise ValueError("La clé 'api_keys_ocr' est invalide ou vide dans le fichier de configuration.")
    

    # Get the first api key in the array for the ocr
    def get_api_key(self):
        try:
            return self.config_path["api_keys_ocr"][0]
        except (KeyError, IndexError):
            raise ValueError("La clé 'api_keys_ocr' est invalide ou vide dans le fichier de configuration.")