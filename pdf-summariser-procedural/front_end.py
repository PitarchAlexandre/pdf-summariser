import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from convert_pdf import convert_pdf_text, max_word, parameter_prompt, configure, api_informations, resume
#https://www.youtube.com/watch?v=PIaccbMT6fo
#https://ttkbootstrap.readthedocs.io
#https://www.geeksforgeeks.org/how-to-center-a-window-on-the-screen-in-tkinter/
#https://www.geeksforgeeks.org/python-tkinter-checkbutton-widget/
#https://stackoverflow.com/questions/66576662/how-to-switch-between-dark-and-light-ttk-theme
#https://www.pythontutorial.net/tkinter/tkinter-separator/
# https://www.tutorialspoint.com/python/tk_anchors.htm

# Creates the main window
app = ttk.Window("solar")
window_width = 700
window_height = 750
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
app.geometry(f"{window_width}x{window_height}+{x}+{y}")
app.title("Summariser")

top_frame = ttk.Frame(app)
top_frame.pack(pady=10, fill=X)

label_title = ttk.Label(top_frame, text="Summariser", font=("Arial", 20, "bold"))
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
    elif language == "english":
        language = "english"
    elif language == "deutsch":
        language = "german"
    else:
        messagebox.showerror("Error", "You must chose a language.")
        return
    
    text_box.delete(1.0, "end")
    pdf_text = convert_pdf_text()

    # Ask to the user the number maximum of words he wants in his summary
    number_max_word = max_word()

    # Prepare the prompt for the ai model
    prompt = parameter_prompt(pdf_text, number_max_word, language)
    
    # Configure the API
    API_KEY, BASE_URL = configure()
    client = api_informations(API_KEY, BASE_URL)
    summary = resume(client, prompt)
    
    # Show the text inn the text zone
    text_box.insert("1.0", summary)

# Bouton pour sélectionner un fichier PDF et générer le résumé
ttk.Button(button_chose_pdf, text="Sélectionner fichier PDF", bootstyle=SUCCESS, command=on_button_click).pack(padx=10, pady=10)

# Cadre pour le bouton "Cancel"
button_frame = ttk.Frame(app)
button_frame.pack(pady=10, padx=10, fill=X, anchor=S) #anchor=S to position the button at the bottom 
ttk.Button(button_frame, text="Cancel", bootstyle=DANGER, command=app.quit).pack(side=RIGHT, padx=50, pady=10)

# start the app (launcher)
app.mainloop()