from openai import OpenAI
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader
from tkinter import simpledialog
#https://docs.python.org/3/library/tkinter.messagebox.html
#https://platform.openai.com/docs/api-reference/introduction
#https://platform.openai.com/docs/overview
#https://ollama.com/
#https://pdfreader.readthedocs.io/en/latest/tutorial.html

def configure():
    load_dotenv()
    API_KEY=os.getenv('API_KEY')
    BASE_URL=os.getenv('BASE_URL')
    return API_KEY, BASE_URL 

# parameters IA
def api_informations(API_KEY,BASE_URL):
    client = OpenAI(
        base_url =BASE_URL,
        api_key=API_KEY # required, but unused when you use ollama in local
    )
    return client

def convert_pdf_text():
    pdf_file = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("pdf files", "*.pdf"), ("all files", "*.*")))
    reader = PdfReader(pdf_file)
    page = reader.pages
    document = ""
    for p in page:
        text = p.extract_text()
        document+=text
    return document

def max_word():
    tk.messagebox.showwarning(title="Infos", message="Les fichiers doivent contenir un maximum de 1400 mots")
    try:
        warning_message = ""
        while True:
            # l'avantage de la fonction askinteger, c'est qu'elle controle directement que le nombre soit un int et évite les mauvaises entrées
            number_max_word = simpledialog.askinteger(title="Nombre de mots", prompt=f"{warning_message}Inserérez le nombre maximum de mots du résumé : ")
            if number_max_word >= 0 and number_max_word <= 1400:   
                return number_max_word
            else:
                 warning_message += "Entrez un nombre entre 0 et 1400.\n"
                 True
    except ValueError as e:
        print(f"An error occured: {e}. La valeur inséré n'est pas valide.")
        tk.messagebox.showerror(title="Error", message="La valeur inséré n'est pas valide"  ) 

def parameter_prompt(document, p_number_max_word, language):
    if p_number_max_word > 0:
        number_word = f" en maximum {p_number_max_word} mots "
    else:
        number_word=""
    prompt=[        
                {"role": "system", "content": """You are a bot which translate texts. You receive texts. Your sole aim is to make summaries. 
                                                These summaries should help you understand the text."You receive texts that were previously in PDF files,
                                                 but have now been converted into text files. If there are chapters, you don't have to name them one by one,
                                                 but summarize the whole text. You must not give your opinion or interpret in your own way.
                                                 You have to start your sentence by \"Here is a word summary in {number_word} words\" in {language}.
                                                You must not exceed the word count. Do not write more than {number_word}""" },
                {"role": "user", "content": f"Summarize the following text :\n{document}\nWrite in {language} and in maximum {number_word} words." }
    ]
    return prompt

def resume(client, prompt):
    stream = client.chat.completions.create(
                model="llama3.2",
                messages=prompt,
                temperature=0,
                #max_tokens=1000,
                stream=True,
    )
    summary = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            summary+=chunk.choices[0].delta.content
    return summary





