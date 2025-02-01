from tkinter import messagebox
import os
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader
from tkinter import simpledialog
from PyPDF2 import PdfFileReader
import ocrmypdf
#https://docs.python.org/3/library/tkinter.messagebox.html
#https://github.com/py-pdf/pypdf
#https://pdfreader.readthedocs.io/en/latest/tutorial.html
#https://courspython.com/classes-et-objets.html
#https://datacorner.fr/pdf/
#https://jonathansoma.com/everything/pdfs/ocr-tools/
    
class PdfFile():
    def __init__(self):
        pass
    
    # Open the file explorateur to choose a PDF file
    @staticmethod
    def select_pdf_file():
        pdf_file = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("pdf files", "*.pdf"), ("all files", "*.*")))
        return pdf_file
    
    # Convert the pdf file in txt file
    @staticmethod
    def convert_pdf_text(pdf_file):
        if not pdf_file:
            raise ValueError("Aucun fichier PDF selectionnné.")
        reader = PdfReader(pdf_file)
        page = reader.pages
        document = ""
        for p in page:
            text = p.extract_text()
            document+=text
        # If the document is empty, the pdf is readen with an OCR reader
        # Unfortunalty, this OCR reader barely works... But it's free! 
        output_pdf = ""
        
        if document == "":
            try:
                ocrmypdf.ocr(pdf_file, output_pdf, language="fra", deskew=True)
                print(f"OCR terminé ! PDF enregistré sous : {output_pdf}")
            except Exception as e:
                print(f"Erreur lors de l'OCR : {e}")
        return document
    
    @staticmethod
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
            tk.messagebox.showerror(title="Error", message=f"La valeur inséré n'est pas valide.\n{e}"  ) 

