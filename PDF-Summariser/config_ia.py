from python_json_config import ConfigBuilder 
import json
# https://pypi.org/project/python-json-config/
# https://www.geeksforgeeks.org/append-to-json-file-using-python/
# https://youtube.com/watch?v=wfopJdI_cFo

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        #load the json file
        self.model_config = self.parse_config(config_path)

    def parse_config(self, config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Le fichier de configuration {config_path} est introuvable.")
        except json.JSONDecodeError:
            raise ValueError("Erreur lors du décodage du fichier JSON.")

    # To have the first config(Ollama, Llama3.2)
    def get_default_config(self):
        try:
            return self.model_config["model_config"][0]
        except (KeyError, IndexError):
            raise ValueError("La clé 'model_config' est invalide ou vide dans le fichier de configuration.")
    
    def get_all_models(self):
        return self.model_config.get("model_config", [])


    def select_ai_model(self, config_path, ai_model):
        with open(config_path, 'r') as f:
            config_list = json.load(f)

        for selected_model in config_list["model_config"]:
            if selected_model["model"] == ai_model:
                return selected_model
    
    def add_model(self, api_key, ai_model, base_url):
        new_config = {
            "api_key": api_key,
            "model": ai_model,
            "base_url": base_url
        }
        model_config = self.load_config()
        model_config["model_config"].append(new_config)
        # Sauvegarder les nouvelles configurations
        self.save_config(model_config)

    def load_config(self):
        try:
            # Ouvre et charge la configuration du fichier JSON
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Si le fichier n'existe pas, retourne une structure par défaut
            return {"model_config": []}
        except json.JSONDecodeError:
            raise ValueError("Erreur lors du décodage du fichier JSON.")


    def save_config(self, model_config):
        try:
            # Sauvegarder le fichier JSON avec le modèle configuré
            with open(self.config_path, 'w') as f:
                json.dump(model_config, f, indent=4)
        except IOError:
            raise ValueError(f"Impossible de sauvegarder le fichier {self.config_path}.")

    def get_selected_model_details(self, selected_model_name):
        model_config = self.load_config()
        for model in model_config["model_config"]:
            if model["model"] == selected_model_name:
                try:
                    print("Détails du modèle sélectionné :", model)
                    return model
                except FileNotFoundError:
                    raise ValueError("Le modèle n'a pas été trouvé.")
        raise ValueError("Le modèle n'a pas été trouvé.")

    def remove_selected_model(self, ia_model):
        model_config = self.load_config()
        updated_model_config = []
    
        for model in model_config["model_config"]:
            if model["model"] != ia_model:
                updated_model_config.append(model)
        
            model_config["model_config"] = updated_model_config
            self.save_config(model_config)
    