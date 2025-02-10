import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from pdf import PdfFile
from ia_client import IAClient
from config_ia import ConfigManager
#https://www.youtube.com/watch?v=PIaccbMT6fo
#https://ttkbootstrap.readthedocs.io
#https://github.com/israel-dryer/ttkbootstrap
#https://www.geeksforgeeks.org/how-to-center-a-window-on-the-screen-in-tkinter/
#https://www.geeksforgeeks.org/python-tkinter-checkbutton-widget/
#https://www.geeksforgeeks.org/how-to-close-a-tkinter-window-with-a-button/
#https://stackoverflow.com/questions/66576662/how-to-switch-between-dark-and-light-ttk-theme
#https://www.pythontutorial.net/tkinter/tkinter-separator/
#https://www.tutorialspoint.com/python/tk_anchors.htm
#https://youtube.com/watch?v=wfopJdI_cFo
#https://youtube.com/watch?v=wfopJdI_cFo
#https://esig.degroote.ch/mardi-3-decembre-2024/pratique-api/installation-package-openai-et-test
#https://docs.python.org/fr/3.13/library/tkinter.ttk.html#
# pour le logo : https://www.flaticon.com/fr/chercher?word=livre
# InstallForge pour la création de l'installeur

# MAIN WINDOW
# Creates the main window
app = ttk.Window("solar")
window_width = 700
window_height = 750
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
app.geometry(f"{window_width}x{window_height}+{x}+{y}")
app.title("PDF Summariser")

top_frame = ttk.Frame(app)
top_frame.pack(pady=10, fill=X)

# HEADER
label_title = ttk.Label(top_frame, text="PDF Summariser", font=("Arial", 20, "bold"))
label_title.pack(pady=3)

# To change light and night mod
def on_toogle_click():
    if check_var.get() == 1:
        ttk.Style("solar")
    else:
        ttk.Style("minty")

# Toogle button
check_var = ttk.IntVar()
checkbox_frame = ttk.Frame(top_frame)
checkbox_frame.pack(padx=30, anchor=NE)
ttk.Checkbutton(checkbox_frame, bootstyle="round-toggle-warning", text="Theme", variable=check_var, onvalue=1, offvalue=0, command=on_toogle_click).pack(side=RIGHT)

separator = ttk.Separator(app, orient=HORIZONTAL)
separator.pack(fill=X)

# IA NEW MODEL WINDOW
def open_add_model_window():
    add_model_window = ttk.Toplevel(app)

    add_model_window_width = 400
    add_model_window_height = 300
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    add_model_window.geometry(f"{add_model_window_width}x{add_model_window_height}+{x}+{y}")
    add_model_window.title("Ajouter un nouveau model IA")
    
    ttk.Label(add_model_window, text="API Key:").pack(pady=5)
    api_key_entry = ttk.Entry(add_model_window, width=40)
    api_key_entry.pack(pady=5)
    
    ttk.Label(add_model_window, text="Nom du modèle IA:").pack(pady=5)
    ai_model_entry = ttk.Entry(add_model_window, width=40)
    ai_model_entry.pack(pady=5)
    
    ttk.Label(add_model_window, text="Base URL:").pack(pady=5)
    base_url_entry = ttk.Entry(add_model_window, width=40)
    base_url_entry.pack(pady=5)

    # Add the new ia in the config.json file
    def add_model_to_config():
        api_key = api_key_entry.get()
        ai_model = ai_model_entry.get()
        base_url = base_url_entry.get()

        config_manager = ConfigManager("config.json")
        config_manager.add_model(api_key, ai_model, base_url)
        config_manager.load_config()

        list_model_name = get_models_combobox()
        combobox_model_ai.config(values=list_model_name)

        messagebox.showinfo(SUCCESS, "Le nouveau modèle a été ajouté avec succès.")
        add_model_window.destroy()

    # Frame of the buttons in the new window
    frame_button_add_model = ttk.Frame(add_model_window)
    # Button to add a new ia model
    frame_button_add_model.pack(padx=10,pady=10,anchor=S) 
    ttk.Button(frame_button_add_model, text="Ajouter le modèle", bootstyle=SUCCESS, command=add_model_to_config).pack(pady=10, padx=5, side=LEFT)
    # Cancel button
    ttk.Button(frame_button_add_model, text="Cancel", bootstyle=DANGER, command=add_model_window.destroy).pack(pady=10, padx=5,side=RIGHT)

def delete_ai_model():
    model_to_delete = combobox_model_ai.get()
    config_manager = ConfigManager("config.json")

    if not model_to_delete:
        messagebox.showerror("Erreur", "Veuillez sélectionner un modèle à supprimer.")
        return
    elif model_to_delete == "llama3.2":
        messagebox.showerror("Erreur", "Vous ne pouvez pas effacer le modèle par défaut.")
        return    
    
    config_manager.remove_selected_model(model_to_delete)

    list_model_name = get_models_combobox()
    combobox_model_ai.config(values=list_model_name)
    combobox_model_ai.set("")

    messagebox.showinfo(SUCCESS, "Le modèle a été effacé avec succès.")
    
# BUTTON insert new ia model
button_model_frame = ttk.Frame(app)
button_model_frame.pack(padx=5,pady=5, anchor=NW) 
ttk.Button(button_model_frame, text="Insérer un nouveau model IA", bootstyle=WARNING, command=open_add_model_window).grid(row=0, column=0, padx=10)
ttk.Button(button_model_frame, text="Effacer model IA", width=15, bootstyle=DANGER, command=delete_ai_model).grid(row=0, column=1, padx=10)

# Combobox IA Models
def get_models_combobox():
    config_manager = ConfigManager("config.json")
    model_list = config_manager.get_all_models()
    list_model_name = []
    for m in model_list:
        model_name = m.get("model")
        list_model_name.append(model_name)
    return list_model_name

list_model_name = get_models_combobox()

combobox_model_ai = ttk.Combobox(app, width=30, height=5, values=list_model_name)
combobox_model_ai.pack(padx=70, pady=5, anchor=NW)


button_chose_pdf = ttk.Frame(app)
button_chose_pdf.pack(pady=5, padx=10, fill=X)

languages = ["français", "english", "deutsch"]
combobox_language = ttk.Combobox(app, bootstyle="success", values=languages)
combobox_language.pack(pady=5)

resume_frame = ttk.Frame(app)
resume_frame.pack(pady=20, padx=15, fill=BOTH, expand=True)
ttk.Label(resume_frame, text="Résumé", font=20).pack(padx=5)

text_box = ttk.Text(resume_frame, height=20, width=70)
text_box.pack(fill=BOTH, expand=True, padx=45, pady=20)

# Fonction which works when the summerize button is pressed
def on_button_click():
    language = combobox_language.get()
    if language == "français":
        language = "french"
        lang = "fra"
    elif language == "english":
        language = "english"
        lang = "eng"
    elif language == "deutsch":
        language = "german"
        lang = "deu"
    else:
        messagebox.showerror("Error", "Vous de devez choisir une langue.")
        return
    


    # Delete all the text in the textbox
    text_box.delete(1.0, "end")

    # Configure the API
    config_manager = ConfigManager("config.json")
    model_ia_selected = combobox_model_ai.get()
    # Takes the ollama and llama3.2 by default
    if not model_ia_selected:
        config = config_manager.get_default_config()
        api_key = config["api_key"]
        ai_model = config["model"]
        base_url = config["base_url"]
    else:
        config = config_manager.get_selected_model_details(model_ia_selected)
        api_key = config["api_key"]
        ai_model = config["model"]
        base_url = config["base_url"]

    # Loads the PdfFile
    pdf_file_selected = PdfFile.select_pdf_file()
    pdf_text = PdfFile.convert_pdf_text(pdf_file_selected, lang)

    # Ask to the user the number maximum of words he wants in his summary
    number_max_word = PdfFile.max_word()
    
    # Create an object of IAClient with the information configurations
    ia_client = IAClient(api_key, base_url, language)
    # Create and configure the api_key and url of the bot
    client = ia_client.create_bot()
    
    prompt = ia_client.parameter_prompt(number_max_word, pdf_text, language)

    # Show the text inn the text zone
    ia_client.generate_summary(client, ai_model, prompt, text_box)

# Bouton pour sélectionner un fichier PDF et générer le résumé
ttk.Button(button_chose_pdf, text="Sélectionner fichier PDF", bootstyle=SUCCESS, command=on_button_click).pack(padx=10, pady=10)

# Cadre pour le bouton "Cancel"
button_frame = ttk.Frame(app)
button_frame.pack(pady=10, padx=10, fill=X, anchor=S) #anchor=S to position the button at the bottom 
ttk.Button(button_frame, text="Quitter", bootstyle=DANGER, command=app.quit).pack(side=RIGHT, padx=50, pady=10)

# start the app (launcher)
app.mainloop()