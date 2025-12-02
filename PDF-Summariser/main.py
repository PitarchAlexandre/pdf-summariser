import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from pdf import PdfFile
from ia_client import IAClient
from config_ia import ConfigManager
from registered_file import DocFile
from chat_bot import ChatBot
import os
from PIL import ImageTk, Image
from ollama_manager import OllamaManager
# Now I have to add the functionnality to translate the frontend text
import gettext

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
#https://docs.python.org/fr/3.13/library/tkinter.ttk.html
#https://docs.python.org/3/library/dialog.html#native-load-save-dialogs
#https://stackoverflow.com/questions/51455765/how-to-build-multiple-py-files-into-a-single-executable-file-using-pyinstaller
# For the logo : https://www.flaticon.com/fr/chercher?word=livre
# InstallForge the creation of the installer https://www.youtube.com/watch?v=ThTs89okfSY 



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
app.iconbitmap("ico/logo.ico")

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
    # TODO add_model_window.iconbitmap("ico/logo.icoico")
    
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

        if api_key == "ollama":
            messagebox.showinfo("Ollama", "Le modèle Ollama va être téléchargé. Cela peut prendre quelques minutes.")
            ollama_manager.pull_model(ai_model)

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

text_box = ttk.ScrolledText(resume_frame, height=20, width=70, wrap=WORD)
text_box.pack(fill=BOTH, expand=True, padx=45, pady=20)

# Function which returns the selected langage 
def get_language():
    # The "language" variable is used to communicate with the AI
    # The "lang_ocr" variable is used because it has to
    # be written this way to get the language in parameter with Tesseract-OCR
    # You can check the documentation to put some other language in parmaters
    # https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
    language = combobox_language.get()
    if language == "français":
        language_selected = {
                        "language" : "french",
                        "lang_ocr" : "fra"   
                    }
        return language_selected
    
    elif language == "english":
        language_selected = {
                        "language" : "english",
                        "lang_ocr" : "eng"   
                    }
        return language_selected
    
    elif language == "deutsch":
        language_selected = {
                        "language" : "german",
                        "lang_ocr" : "deu"   
                    }
        return language_selected

# Function which works when the summerize button is pressed
def on_button_click_select_pdf_file():
    language_dictionnary = get_language() 
    if language_dictionnary == None:
        messagebox.showerror("Error", "Vous de devez choisir une langue.")
        return

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

    global pdf_file_selected 
    # Loads the PdfFile
    pdf_file_selected = PdfFile.select_pdf_file()
    pdf_text = PdfFile.convert_pdf_text(pdf_file_selected, language_dictionnary["lang_ocr"])

    # Ask to the user the number maximum of words he wants in his summary
    number_max_word = PdfFile.max_word()
    
    # Delete all the text in the textbox
    text_box.delete(1.0, "end")
    
    # Create an object of IAClient with the information configurations
    ia_client = IAClient(api_key, ai_model, base_url, language_dictionnary["language"], pdf_text)
    # Create and configure the api_key and url of the bot
    client = ia_client.create_bot()

    prompt = ia_client.parameter_prompt(number_max_word)

    global summary
    # Show the text inn the text zone
    summary = ia_client.generate_summary(client, ai_model, prompt, text_box)

    ia_client.get_ai_client()

    # it used to send what's been written to the chatbot
    global api_key_used
    global ai_model_used
    global base_url_used
    global language_dictionnary_used
    global pdf_text_used

    api_key_used = api_key
    ai_model_used = ai_model
    base_url_used = base_url
    language_dictionnary_used = language_dictionnary["language"]
    pdf_text_used = pdf_text

    global ia_client_used
    ia_client_used = client
    global prompt_used
    prompt_used = prompt

# Button to select a PDF file and generate the summary
ttk.Button(button_chose_pdf, text="Sélectionner fichier PDF", bootstyle=SUCCESS, command=on_button_click_select_pdf_file).pack(padx=10, pady=10)

def on_button_click_generate_document():
    try:
        file_name = os.path.basename(pdf_file_selected)
    except:
        messagebox.showerror(title="Error", message="Erreur : \n  Aucun fichier n'a été inséré. \n" +
                             "Veuillez sélectionner un fichier pdf afin de générer un fichier.")
    
    summary_file = DocFile(file_name, summary)
    DocFile.create_file(summary_file)

# There's a lot of stuff to improve here
def chat_with_bot(bot_text_box, user_text):
    try:
        if 'summary' in globals() and summary:
            context = summary
        else:
            context = "No summary. You are just a chat bot."

        if get_language () != None:
            language_dictionnary = get_language() 
            if language_dictionnary == None:
                messagebox.showerror("Error", "Vous de devez choisir une langue.")
                return
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
            # Create an object of IAClient with the information configurations
            chat_bot = ChatBot(api_key, ai_model, base_url, language_dictionnary["language"], None, "No summary. You are just a chat bot.")
            # Create and configure the api_key and url of the bot
            chat_bot_client = chat_bot.create_bot()

            context = chat_bot.receive_context(prompt_used)

        chat_bot.answer(chat_bot_client, ai_model, context, user_text, bot_text_box)

    except Exception as e:
        messagebox.showerror(
            title="Erreur critique",
            message=f"Erreur lors de l'initialisation du bot.\nVeuillez sélectionner un model ia et une lange."
                    f"\nSi vous en avez sélectionné, il se peut que la clé API ou l'URL soient mals configurés.\nError : {e}"
    )
        print(f"Erreur lors de l'initialisation du bot : {e}")

# WINDOW FOR THE DISCUSSION WITH THE BOT
# IA NEW MODEL WINDOW
def on_button_click_talk_to_bot():
    if 'prompt_used' not in globals() or prompt_used is None or summary == None:
        messagebox.showerror("Error", "Veuillez d'abord générer un résumé avant d'utiliser le chatbot.")
        return
    chat_with_bot_window = ttk.Toplevel(app)

    chat_with_window_width = 700
    chat_with_window_height = 500
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    chat_with_bot_window.geometry(f"{chat_with_window_width}x{chat_with_window_height}+{x}+{y}")
    chat_with_bot_window.title("Talk to SumBot!")
    chat_with_bot_window.iconbitmap("ico/logo.ico")
    
    #Create the bot's image
    global bot_image
    try:
        bot_image = Image.open("img/bot.png").resize((50,50))
        bot_image = ImageTk.PhotoImage(bot_image)
    except Exception as e:
        print("Image not loaded")
        bot_image = None

    # Bot frame
    frame_chat_bot_output_wnd = ttk.Frame(chat_with_bot_window)
    frame_chat_bot_output_wnd .pack(padx=10, pady=15, anchor=N, fill=BOTH, expand=True)
    if bot_image:
        ttk.Label(frame_chat_bot_output_wnd , image=bot_image).pack(padx=20, pady=60, side=LEFT)
    bot_chat_answer = ttk.ScrolledText(frame_chat_bot_output_wnd , height=15, width=80, wrap=WORD)
    bot_chat_answer.pack(fill=BOTH, expand=True, padx=5, pady=5)
    # Show the summarise in the frame 
    try:
        bot_chat_answer.insert(tk.END, summary)
    except Exception as e:
        print("La variable 'summary' est vide.", e)

    # User's input
    frame_user_input_chat_bot_wnd = ttk.Frame(chat_with_bot_window)
    frame_user_input_chat_bot_wnd.pack(padx=10,pady=10,anchor=S, fill=X,expand=False)
    ttk.Label(frame_user_input_chat_bot_wnd, text="Ecrivez :").pack(padx=25, pady=60, side=LEFT)
    user_chat_entry = ttk.ScrolledText(frame_user_input_chat_bot_wnd, height=5, width=80, wrap=WORD)
    user_chat_entry.pack(fill=BOTH, expand=True, padx=5,pady=5)
    
    # To get the text in the scrolledtext box
    def on_send_button_click():
        user_chat_text = user_chat_entry.get("1.0", tk.END)
        user_chat_entry.delete(1.0, "end")
        bot_chat_answer.insert(tk.END, "\n\n - " + user_chat_text)
        chat_with_bot(bot_chat_answer, user_chat_text) 
        
        
    ttk.Button(frame_user_input_chat_bot_wnd, text="Envoyer", bootstyle=INFO, command=on_send_button_click).pack(pady=5, padx=25,side=RIGHT)
    
    ttk.Button(chat_with_bot_window, text="Cancel", bootstyle=DANGER, command=chat_with_bot_window.destroy).pack(pady=15, padx=15,side=RIGHT)


# Frame for the two buttons of the bottom
frame_bottom_bottoms = ttk.Frame(app)
frame_bottom_bottoms.pack(pady=10, padx=10, fill=X, anchor=S) #anchor=S to position the button at the bottom 
# Button the "Generate document" Button
ttk.Button(frame_bottom_bottoms, text="Générer un document", bootstyle=INFO, command=on_button_click_generate_document).pack(side=LEFT, padx=50, pady=1)
# Button to talk to a bot
ttk.Button(frame_bottom_bottoms, text="Discuter avec SumBot", bootstyle="success-outline", command=on_button_click_talk_to_bot).pack(side=LEFT, expand=True, padx=50, pady=5)
# Button the "Quit" Button
ttk.Button(frame_bottom_bottoms, text="Quitter", bootstyle=DANGER, command=app.quit).pack(side=RIGHT, padx=50, pady=5)

if __name__ == "__main__":
    # opens ollama
    ollama_manager = OllamaManager()
    ollama_manager.start()

    # start the app (launcher)
    app.mainloop()
    